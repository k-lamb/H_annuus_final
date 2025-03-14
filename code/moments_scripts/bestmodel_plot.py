
import os
import sys
import pandas as pd # type: ignore
import numpy as np # type: ignore
from socketserver import ThreadingUnixDatagramServer
import time
import random

import demes, demesdraw, matplotlib.pylab as plt # type: ignore

Pair_name = sys.argv[1]
model = sys.argv[2]
complexity = sys.argv[3]
ancient_exp = sys.argv[4]
shelf = sys.argv[5]
TV_exp = sys.argv[6]
selfing = sys.argv[7]
selfing_all = sys.argv[8]
save_folder = sys.argv[9]
mig_epoch = sys.argv[10]
pulse = sys.argv[11]
wd = r"/global/scratch/users/kericlamb/Hannuus_moments3" # working directory character string

model_str = str("{model}_{complexity}_{ancient_exp}_{shelf}_{TV_exp}_TV_{selfing}_WildAnc_{selfing_all}_admix_{pulse}".format(model=model, complexity=complexity, ancient_exp=ancient_exp, shelf=shelf, TV_exp=TV_exp, selfing=selfing, selfing_all=selfing_all, pulse=pulse))
data = pd.read_csv("{wd}/data/moments_outputs/{save_folder}/{Pair_name}_{model_str}.txt".format(wd=wd, save_folder=save_folder, Pair_name=Pair_name, model_str=model_str), sep='\t')
best_model = data.loc[data["AIC"].idxmin()]

# Load the template text
with open('{wd}/code/moments_scripts/models/model_templates/{model_str}_template.yaml'.format(wd=wd, model_str=model_str), 'r') as file:
    template = file.read()

# Re-write template with data from the best model (by AIC)
placeholders = [f"{{{key}}}" for key in best_model.index]
escaped_template = template.replace('{', '{{').replace('}', '}}') # doing something kinda wonky to deal with escaping brackets for migration models
for ph in placeholders:
    escaped_template = escaped_template.replace(f"{{{{{ph[1:-1]}}}}}", ph)

deme_model = escaped_template.format(**best_model.to_dict())

output_filename = "{wd}/data/moments_outputs/plots/best_models/{save_folder}/{Pair_name}_{model_str}_best.yaml".format(wd=wd, save_folder=save_folder, Pair_name=Pair_name, model_str=model_str)
with open(output_filename, 'w') as output_file:
    output_file.write(deme_model)
print(f"File created: {output_filename}")

graph = demes.load(output_filename)
demesdraw.tubes(graph, log_time=True, num_lines_per_migration=10)
plt.savefig("{wd}/data/moments_outputs/plots/best_models/{save_folder}/{Pair_name}_{model_str}_best.png".format(wd=wd, save_folder=save_folder, Pair_name=Pair_name, model_str=model_str), dpi=300)
plt.close()
