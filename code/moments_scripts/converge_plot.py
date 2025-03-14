import os
import sys
import pandas as pd # type: ignore
import numpy as np # type: ignore
from socketserver import ThreadingUnixDatagramServer
import time
import random

import demes, demesdraw, matplotlib.pylab as plt # type: ignore

wd = "/Users/kericlamb/Documents/Work MacBook/Research/paper_code/H_annuus_demography" # working directory character string
model_run = sys.argv[1]
con_best = sys.argv[2] # whether to take the converged model "con" or the best model "best" by AIC
file_path = "{0}/data/moments_outputs/{1}".format(wd, model_run)

files = [ 
    f for f in os.listdir(file_path)
    if os.path.isfile(os.path.join(file_path, f)) and f.startswith("TV.Wild")
]

# Check if the folder exists, and create it if it doesn't
save_path = "{0}/converged_model_plots".format(file_path)

if not os.path.exists(save_path):
    os.makedirs(save_path)  # Creates the folder and any necessary parent folders
    print(f"Folder created: {save_path}")
else:
    print(f"Folder already exists: {save_path}")

# loop through all models
for i in range(len(files)):
    dat = pd.read_csv("{0}/{1}".format(file_path, files[i]), sep="\t")
    dat["model_full"] = dat["model"] + dat["complexity"] + dat["ancient_exp"] + dat["shelf"] + dat["TV_exp"] + dat["selfing"] + dat["selfing_all"]

    # find converged model solution
    if con_best == "con":
        mode_value = dat["AIC"].mode()[0]  # Get the first mode value (there could be multiple modes)
        rows_with_mode = dat[dat["AIC"] == mode_value]
        converged_model = rows_with_mode.head(1)
        converged_model = converged_model.iloc[0]
    
    if con_best == "best":
        converged_model = dat.loc[dat["AIC"].idxmin()]

    with open('{0}/model_templates/{1}_template.yaml'.format(file_path, files[i].replace(".txt", "").replace("TV.Wild_", "")), 'r') as file:
        template = file.read()
    
    # inserting values into templates
    placeholders = [f"{{{key}}}" for key in converged_model.index]
    escaped_template = template.replace('{', '{{').replace('}', '}}') # doing something kinda wonky to deal with escaping brackets for migration models
    for ph in placeholders:
        escaped_template = escaped_template.replace(f"{{{{{ph[1:-1]}}}}}", ph)
    deme_model = escaped_template.format(**converged_model.to_dict())

    # saving yaml and png of converged model
    if con_best == "con":
        if not os.path.exists(save_path+"/converged"): os.makedirs(save_path+"/converged")
        output_filename = "{0}/{1}".format(save_path+"/converged", files[i].replace(".txt", "").replace("TV.Wild_", ""))
    if con_best == "best":
        if not os.path.exists(save_path+"/best"): os.makedirs(save_path+"/best/")
        output_filename = "{0}/{1}".format(save_path+"/best", files[i].replace(".txt", "").replace("TV.Wild_", ""))

    with open("{0}.yaml".format(output_filename), 'w') as output_file:
        output_file.write(deme_model)
    print(f"File created: {output_filename}")

    graph = demes.load("{0}.yaml".format(output_filename))
    demesdraw.tubes(graph, log_time=True, num_lines_per_migration=2)
    plt.savefig("{0}.png".format(output_filename), dpi=300)
    plt.close()





