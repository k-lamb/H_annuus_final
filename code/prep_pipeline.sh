#!/usr/bin/bash
#SBATCH -J pipe_prep
#SBATCH -p savio2_htc
#SBATCH -a co_rosalind
#SBATCH -n 1
#SBATCH -t 00:10:00
#SBATCH --mem=8G
#SBATCH -o /global/scratch/users/kericlamb/Hannuus_moments3/data/moments_outputs/out/prep_out_%j.txt
#SBATCH -e /global/scratch/users/kericlamb/Hannuus_moments3/data/moments_outputs/error/prep_error_%j.txt

### sbatch --array=1 prep_pipeline.sh full_run save_folder # debug or full_run // where you want to save plots and data to

### H. annuus demographic inference in wild and traditional varieties
# PIPELINE: 
# 0 - FILE ORGANIZATION: currently works within a directory that has folders for ./code; ./data (./data/moments_outputs; ./data/moments_outputs/out; ./data/moments_outputs/error); and ./VCFs
#   i - ./code should contain: popmap.R; metadata.R; VCF_missing_inds.R; projection_digest.py; scripts for Moments models should be stored in a folder within code: ./code/moments_scripts
#  ii - ./data should be empty before running
# iii - ./VCFs should have VCF file (test_vcf.vcf) -- can make this more flexible as needed
# 1 - VCF FILTERING: remove individuals with excess missing data
#   i - run VCF_missing_inds.R, which saves a 2-col data frame with individuals where missing < threshold (missing arg below)
#  ii - keep only individuals in ind_missing_threshold.txt using bcftools filter
# 2 - PROJECTION & METADATA: determine optimal projection for Moments and save in useable format
#   i - create easySFS environment and downloads (as needed) easySFS script, then generates a popmap using the VCF... can modify popmap.R for more complex population maps
#  ii - runs easySFS and saves/digests output into .csv (easySFS_output_processed.csv), then generates a metadata file for Moments runs
# 3 - DEMO. INFER.: run Moments and save data
#   i - create/access Moments environment, then initializes an array job that runs all models (Hannuus.sh/.py for more details)

# 1 - VCF FILTERING
module load r/4.4.0-gcc-11.4.0 # for determining individuals to filter
module load bio/bcftools/1.16-gcc-11.4.0 # vcf is in v4, so vcftools does not work

ind_miss=0.2 # cut-off for missing data within individuals for individual to be included in down-stream analyses
vcf_name="test_vcf" # name of VCF to use

cd /global/scratch/users/kericlamb/Hannuus_moments3 # has separate folders for data, VCFs, and code

Rscript ./code/VCF_missing_inds.R $vcf_name $ind_miss # threshold cutoff for proportion sites an individual can have. Exports a df of all missingness & a df of individuals to save
save_ind=$(awk -F'\t' '{print $1}' ./data/ind_missing_threshold.txt | paste -sd ',' -) # comma-separated list of individuals to retain
bcftools view -s ${save_ind} -c 1 ./VCFs/${vcf_name}.vcf -o ./VCFs/${vcf_name}_filter.vcf # retain individuals from save_ind: -s ${save_ind}, remove monomorphic SNPs: -c 1 

module purge

# 2 - PROJECTION AND METADATA CREATION
module load anaconda3/2024.02-1-11.4
module load r/4.4.0-gcc-11.4.0 

easySFS_env="easySFS" # change to name of easySFS python environment if you already have installed.

# checks if easySFS environment exists. if it does, then it activates it. if it does not, it creates it
if conda env list | grep -q "^$easySFS_env "; then
    echo "Environment '$easySFS_env' already exists."
    source activate $easySFS_env
else
    echo "Environment '$easySFS_env' does not exist. Creating it..."
    conda create -n easySFS
    source activate easySFS
    conda install -c conda-forge numpy pandas scipy -y
    git clone https://github.com/isaacovercast/easySFS.git
    cd easySFS
    chmod 777 easySFS.py
    cd .. 
    if [ $? -eq 0 ]; then
        echo "Environment '$easySFS_env' created successfully."
    else
        echo "Failed to create environment '$easySFS_env'. Please check for errors."
    fi
fi

Rscript ./code/popmap.R $vcf_name # generates a popmap with the filtered VCF generated here, unless one already exists

python ./easySFS/easySFS.py -i ./VCFs/${vcf_name}_filter.vcf -p ./data/popmap.txt -o ./data -f -a --preview > ./data/easySFS_output.txt # runs easySFS, saves output as file in ./data... slow
python ./code/projection_digest.py # digests raw easySFS output into useable table

# creating metadata file:
thresh=0.9 # picks highest projection for SFS within (1-thresh)*100 percent of the maximum number of sites retained
iter=5 # base number of script iterations which will launch to run moments
iter_multiplier=10 # number of times each model will run in loop in H_annuus.py -- doing this to try to cut down on the number of slurm jobs (96 models * iter)

Rscript ./code/metadata.R $thresh ${vcf_name}_filter $iter # takes raw easySFS output and generates metadata file (./data/metadata.txt) for Moments shellscripting 

conda deactivate
module purge

# 3 - MOMENTS/DEMOGRAPHIC INFERENCE
module load anaconda3/2024.02-1-11.4
Moments_env="Moments" # change to name of Moments python environment if you already have installed.

# checks if Moments environment exists. if it does, then it activates it. if it does not, it creates it
if conda env list | grep -q "^$Moments_env "; then
    echo "Environment '$Moments_env' already exists."
    source activate $Moments_env
    module load python/3.11.6-gcc-11.4.0 # requires python 3.8-3.13
    # pip install moments-popgen # can also install from bioconda -- https://pypi.org/project/moments-popgen/
    # pip install demes demesdraw # other dependencies for moments
else
    echo "Environment '$Moments_env' does not exist. Creating it..."
    conda create -n $Moments_env
    source activate $Moments_env
    conda install -c conda-forge numpy pandas scipy -y
    pip install cython mpmath matplotlib networkx ipython # can also conda install most, if not all of these
    module load python/3.11.6-gcc-11.4.0 # requires python 3.8-3.13
    pip install moments-popgen # can also install from bioconda -- https://pypi.org/project/moments-popgen/
    pip install demes demesdraw # other dependencies for moments
    if [ $? -eq 0 ]; then
        echo "Environment '$Moments_env' created successfully."
    else
        echo "Failed to create environment '$Moments_env'. Please check for errors."
    fi
fi

# running Moments:
# generate all model, options, and template files for all models of interest
# creating debug set so we can see how it runs without launching a million files
if [[ $1 == "debug" ]]; then
    model_list=("bi_mig")
    complexity_list=("base") # base hyper
    ancient_exp_list=("anc_noexp")
    shelf_list=("shelf")
    TV_exp_list=("TV_noexp")
    selfing_list=("self")
    template_list=("True" "False")
    iter=1 # overwrites earlier declaration
    iter_multiplier=2 # overwrites earlier declaration
    maxiter=1
    selfing_all_list=("self")
    mig_epoch_list=("1")
    pulse_list=("pulse" "none")
elif [[ $1 == "subset" ]]; then
    model_list=("bi_mig" "uni_mig" "no_mig")
    complexity_list=("hyper")
    ancient_exp_list=("anc_exp")
    shelf_list=("shelf" "noshelf")
    TV_exp_list=("TV_exp" "TV_noexp")
    selfing_list=("self")
    template_list=("True" "False")
    maxiter=1000
    selfing_all_list=("self" "outcross")
    mig_epoch_list=("1")
    pulse_list=("pulse" "none")
elif [[ $1 == "full_run" ]]; then
    model_list=("bi_mig" "uni_mig" "no_mig")
    complexity_list=("base" "hyper") # "base" "hyper"
    ancient_exp_list=("anc_exp" "anc_noexp")
    shelf_list=("shelf" "noshelf")
    TV_exp_list=("TV_exp" "TV_noexp")
    selfing_list=("self")
    template_list=("True" "False")
    maxiter=1000
    selfing_all_list=("self" "outcross")
    mig_epoch_list=("1") # if you want to include "2", need to change scribe folder to model_ext_mig below
    pulse_list=("pulse" "none")
else
    echo "debug, subset, or full_run?"
    exit
fi

# create directories for saving files
save_folder=$2 # requires in-line input for directory that needs to be made to save Hannuus.py runs
echo $save_folder

mkdir -p ./data/moments_outputs/$save_folder
mkdir -p ./data/moments_outputs/plots/best_models/$save_folder

# Loop through all model combinations 
for model in "${model_list[@]}"; do
  for complexity in "${complexity_list[@]}"; do
    for ancient_exp in "${ancient_exp_list[@]}"; do
      for shelf in "${shelf_list[@]}"; do
        for TV_exp in "${TV_exp_list[@]}"; do
          for selfing in "${selfing_list[@]}"; do
            for selfing_all in "${selfing_all_list[@]}"; do
              for mig_epoch in "${mig_epoch_list[@]}"; do
		for pulse in "${pulse_list[@]}"; do
                  python ./code/moments_scripts/models/model_ext/model_scribe_options_ext.py $model $complexity $ancient_exp $shelf $TV_exp $selfing $selfing_all $mig_epoch $pulse
                  python ./code/moments_scripts/models/model_ext/model_scribe_ext.py $model $complexity $ancient_exp $shelf $TV_exp $selfing True $selfing_all $mig_epoch $pulse
                  python ./code/moments_scripts/models/model_ext/model_scribe_ext.py $model $complexity $ancient_exp $shelf $TV_exp $selfing False $selfing_all $mig_epoch $pulse
                  sbatch --array=1-$iter ./code/moments_scripts/Hannuus.sh $model $complexity $ancient_exp $shelf $TV_exp $selfing $iter_multiplier $maxiter $selfing_all $save_folder $mig_epoch $pulse
                done
              done
            done
          done
        done
      done
    done
  done
done

conda deactivate # deactivate moments environment
echo "ended at" `date` # print the time script finishes
