
cd /global/scratch/users/kericlamb/Hannuus_moments3/data/moments_outputs

mkdir $1
mv ./*.txt $1 # clears output files

mkdir ./plots/best_models/$1
mv ./plots/best_models/*.yaml ./plots/best_models/$1
mv ./plots/best_models/*.png ./plots/best_models/$1

mkdir ./out/$1
mkdir ./error/$1
mv ./out/*.txt ./out/$1
mv ./error/*.txt ./error/$1
