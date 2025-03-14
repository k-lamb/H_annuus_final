# general packages. type ignores are because of VS Code
import os
import sys
import pandas as pd # type: ignore
import numpy as np # type: ignore
from socketserver import ThreadingUnixDatagramServer
import time
import random

# demographic inference libraries. type ignores are for VS Code
import moments # type: ignore
from moments import Numerics # type: ignore
from moments import Integration # type: ignore
from moments import Spectrum # type: ignore
from moments import Misc # type: ignore
import demes, demesdraw, matplotlib.pylab as plt # type: ignore

wd = r"/global/scratch/users/kericlamb/Hannuus_moments3" # working directory character string

print(wd)

# define sys args
Pair_name = sys.argv[1]
pop_id1 = sys.argv[2]
pop_id2 = sys.argv[3]
proj_n1 = int(sys.argv[4])
proj_n2 = int(int(sys.argv[5])/1) # divide by 4 to even up sample size. 
vcf = sys.argv[6]
model = sys.argv[7]
maxiter = int(sys.argv[8])
complexity = sys.argv[9]
ancient_exp = sys.argv[10]
shelf = sys.argv[11]
TV_exp = sys.argv[12]
selfing = sys.argv[13]
iter = int(sys.argv[14])
selfing_all = sys.argv[15]
save_folder = sys.argv[16]
mig_epoch = sys.argv[17]
pulse = sys.argv[18]

print("%s model is running" % model)

# load demographic model information
model_str = str("{model}_{complexity}_{ancient_exp}_{shelf}_{TV_exp}_TV_{selfing}_WildAnc_{selfing_all}_admix_{pulse}".format(model=model, complexity=complexity, ancient_exp=ancient_exp, shelf=shelf, TV_exp=TV_exp, selfing=selfing, selfing_all=selfing_all, pulse=pulse))
deme_str = str("{wd}/code/moments_scripts/models/model_yamls/{model_str}_model.yaml".format(wd=wd, model_str=model_str))
deme_options = str("{wd}/code/moments_scripts/models/model_options/{model_str}_options.yaml".format(wd=wd, model_str=model_str))

# setting pop id's and projections
pop_id=[pop_id1,pop_id2]
ns=[proj_n1, proj_n2]

#read in data and create a SFS 
dd = moments.Misc.make_data_dict_vcf("{0}/VCFs/{1}.vcf".format(wd, vcf), "{0}/data/popmap.txt".format(wd))
fs = moments.Spectrum.from_data_dict(dd, pop_ids= pop_id, projections = ns, polarized = False)

# define mutation rate and number of sites from which SNPs were sampled (SNPs*150bp*2 (paired-end))
Ls = len(dd) * 300 # 150bp paired-end reads, approximates number of sites filtered loci come from
us =  6.1e-9 # mutation rate from Peter's CH. 1
uL = np.sum(us * Ls)

for i in range(iter): # number of times to iterate and save to df. doing here to cut down on number of jobs sent to savio
    perturb = random.randint(0,3) # add random perturbation for bigger runs
    print(perturb)
        
    # adding a while True clause because options file is not accepting a constraint. cannot tell why, but re-running till it finds an acceptable Tmig2 suffices for now.
    while True:
        try:
            ret = moments.Demes.Inference.optimize(deme_str, deme_options, fs, uL=uL, perturb=perturb, maxiter=maxiter) # remove maxiter before full run (defaults to 1e3)
            break
        except Exception as e:
            print(f"Error occurred: {e}. Retrying...")
            time.sleep(1)
    
    param_names, opt_params, LL = ret
    AIC = 2 * len(opt_params) - 2 * -LL

    # begin building data to add to existing data file
    row = {'Pair_name': Pair_name, 'model': model} # base information for run
    row.update({param: value for param, value in zip(param_names, opt_params)}) # Add parameter names and values dynamically
    row.update({'ll_model': LL, 'AIC': AIC}) # Add LL and AIC names and parameters
    row.update({'complexity': complexity, 'ancient_exp': ancient_exp, 'shelf': shelf, 'TV_exp': TV_exp, 'selfing':selfing, 'selfing_all':selfing_all, 'mig_epoch':mig_epoch, 'pulse':pulse}) # add all other model data

    # save data
    file_name = "{wd}/data/moments_outputs/{save_folder}/{Pair_name}_{model_str}.txt".format(wd=wd, save_folder=save_folder, Pair_name=Pair_name, model_str=model_str)

    # check if file already exists. if not, create one
    if os.path.exists(file_name):
        print(f"File '{file_name}' already exists. Saving data to existing file.")
        df = pd.read_csv("{0}".format(file_name), sep='\t') 
    else:
        print(f"File '{file_name}' does not exist. Creating it now.")
        with open(file_name, 'w') as file:
            df = pd.read_csv("{0}".format(file_name), sep='\t', header=None, names=param_names) # read in data (doing this here so it is as recent as possible)
            pass

    # df = pd.read_csv("{0}".format(file_name), sep='\t', header=None, names=param_names) # read in data (doing this here so it is as recent as possible)
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv("{0}".format(file_name), index=False, sep="\t", header=True)
