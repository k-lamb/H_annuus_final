#!/usr/bin/bash
#SBATCH -J moments
#SBATCH -p savio2_htc
#SBATCH -a co_rosalind
#SBATCH -n 1
#SBATCH -t 8:00:00
#SBATCH --mem=8G
#SBATCH -o /global/scratch/users/kericlamb/Hannuus_moments3/data/moments_outputs/out/mig_out_%j.txt
#SBATCH -e /global/scratch/users/kericlamb/Hannuus_moments3/data/moments_outputs/error/mig_error_%j.txt

# array size defines number of iterations
### sbatch --array=1-$iter Hannuus_mig.sh # iterations defined in prep_pipeline.sh (~10-50)

# Load conda module
module purge
module load anaconda3/2024.02-1-11.4

Moments_env="Moments" # change to name of Moments python environment if you already have installed.

# checks if Moments environment exists. if it does, then it activates it. if it does not, it creates it
if conda env list | grep -q "^$Moments_env "; then
    echo "Environment '$Moments_env' already exists."
    source activate $Moments_env
    module load python/3.11.6-gcc-11.4.0 # requires python 3.8-3.13
    #  pip install moments-popgen # can also install from bioconda -- https://pypi.org/project/moments-popgen/
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

cd /global/scratch/users/kericlamb/Hannuus_moments3

# activate moments environment
# source activate $Moments_env # change to name of Moments python environment if you installed under different name.

# load the metadata object into memory
metadata=./data/moments_metadata.txt # metadata generated in ./code/prep_pipeline.sh by ./code/metadata.R 

# mining metadata 
Pair=$( cat $metadata  | sed '1d' | sed "${SLURM_ARRAY_TASK_ID}q;d" | awk -F "\t" '{ print $1 }' ) # pair name
pop1=$( cat $metadata  | sed '1d' | sed "${SLURM_ARRAY_TASK_ID}q;d" | awk -F "\t" '{ print $2 }' ) # name of population 1 
pop2=$( cat $metadata  | sed '1d' | sed "${SLURM_ARRAY_TASK_ID}q;d" | awk -F "\t" '{ print $3 }' ) # name of population 2
proj1=$( cat $metadata  | sed '1d' | sed "${SLURM_ARRAY_TASK_ID}q;d" | awk -F "\t" '{ print $4 }' ) # projection for population 1
proj2=$( cat $metadata  | sed '1d' | sed "${SLURM_ARRAY_TASK_ID}q;d" | awk -F "\t" '{ print $5 }' ) # projection for population 2
vcf=$( cat $metadata  | sed '1d' | sed "${SLURM_ARRAY_TASK_ID}q;d" | awk -F "\t" '{ print $6 }' ) # name of the vcf to use

# define inputs to run each model (provided by prep_pipeline.sh)
model=$1 complexity=$2 ancient_exp=$3 shelf=$4 TV_exp=$5 selfing=$6 iter_multiplier=$7 maxiter=$8 selfing_all=$9 save_folder=${10} mig_epoch=${11} pulse=${12} # define all parameters for the model pulling from prep_pipeline.sh
echo $save_folder

echo "beginning Moments runs"
python ./code/moments_scripts/Hannuus.py $Pair $pop1 $pop2 $proj1 $proj2 $vcf $model $maxiter $complexity $ancient_exp $shelf $TV_exp $selfing $iter_multiplier $selfing_all $save_folder $mig_epoch $pulse
python ./code/moments_scripts/bestmodel_plot.py $Pair $model $complexity $ancient_exp $shelf $TV_exp $selfing $selfing_all $save_folder $mig_epoch $pulse

conda deactivate # deactivate moments environment
echo "ended at" `date` # print the time script finishes
