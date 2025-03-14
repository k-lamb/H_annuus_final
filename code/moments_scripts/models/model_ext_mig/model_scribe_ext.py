# this script generates .yaml files for models as well as their templates.

import os
import sys

# # savio
wd = "/global/scratch/users/kericlamb/Hannuus_moments3/code/moments_scripts" # upper level directory
model_wd = "models/model_yamls" # where to save models nested within wd
template_wd = "models/model_templates" # where to save templates nested within wd

# # home system
# wd = "/Users/kericlamb/Documents/Work MacBook/Research/paper_code/H_annuus_demography/Hannuus_moments3_og/code/moments_scripts/models/scribe_mig_ext" # upper level directory
# model_wd = "tests/model_yamls" # where to save models nested within wd
# template_wd = "tests/model_templates" # where to save templates nested within wd

# defining input parameters for creating model files and their templates
model = sys.argv[1] # bi_mig uni_mig or no_mig
complexity = sys.argv[2] # base or hyper
ancient_exp = sys.argv[3] # anc_exp or anc_noexp
shelf = sys.argv[4] # shelf or noshelf
TV_exp = sys.argv[5] # TV_exp or TV_noexp
selfing = sys.argv[6] # self or outcross for TV
template = sys.argv[7] # True or False (whether to make a template (T) or to generate the model script (F))
selfing_all = sys.argv[8] # self or outcross for Anc & Wild
mig_epoch = int(sys.argv[9]) # 1 or 2 epochs of migration for Wild -> TV
overwrite = True # True or False (whether to overwrite existing model & template files)

# defining that "True" == True (needed for sys arguments)
def str_to_bool(s):
    if s == "True":
        return True
    elif s == "False":
        return False

template = str_to_bool(template)

# define model parameters of interest 
if template == True:
    # ancestral population
    T0_anc = "{T0_anc}"
    N0_anc = "{N0_anc}"
    T1_anc = "{T1_anc}"
    N1_anc = "{N1_anc}"
    Tfinal_anc = "{Tfinal_anc}"
    Nfinal_anc = "{Nfinal_anc}"
    self_anc0_rate = "{self_anc0_rate}" 
    self_anc1_rate = "{self_anc1_rate}" 
    self_anc2_rate = "{self_anc2_rate}"

    # Wild population
    T0_Wild = "{T0_Wild}"
    N0_Wild = "{N0_Wild}"
    N0exp_Wild = "{N0exp_Wild}"
    Tcon_Wild = "{Tcon_Wild}"
    Ncon_Wild = "{Ncon_Wild}"
    Nfinal_Wild = "{Nfinal_Wild}"
    N_Wild = "{N_Wild}" # for base only
    self_Wild0_rate = "{self_Wild0_rate}" 
    self_Wild1_rate = "{self_Wild1_rate}" 
    self_Wild2_rate = "{self_Wild2_rate}"

    # TV population
    Tshelf_TV = "{Tshelf_TV}"
    N0_TV = "{N0_TV}"
    Nshelf_TV = "{Nshelf_TV}"
    Ncon_TV = "{Ncon_TV}"
    Tcon_exp_TV = "{Tcon_exp_TV}" # exp only
    Texp_TV = "{Texp_TV}" # exp only
    Nexp_TV = "{Nexp_TV}" # exp only
    self_TV0_rate = "{self_TV0_rate}" 
    self_TV1_rate = "{self_TV1_rate}" 
    self_TV2_rate = "{self_TV2_rate}"

    # Migration
    Tmig_WildTV = "{Tmig_WildTV}"
    Tmig_WildTV2 = "{Tmig_WildTV2}"
    Tmig_TVWild = "{Tmig_TVWild}"
    Mig_WildTV = "{Mig_WildTV}"
    Mig_WildTV2 = "{Mig_WildTV2}"
    Mig_TVWild = "{Mig_TVWild}"

elif template == False: 
    # edit here if parameters are pushing bounds
    
    # ancestral population
    T0_anc = "2.2e5"
    N0_anc = "1e5"
    T1_anc = "7.6e3"
    N1_anc = "8.3e3"
    Tfinal_anc = "5.3e3"
    Nfinal_anc = "1.2e4"
    self_anc0_rate = "0.1" 
    self_anc1_rate = "0.1"  
    self_anc2_rate = "0.1" 

    # Wild population
    T0_Wild = "3.2e3"
    N0_Wild = "1.2e4"
    N0exp_Wild = "2.6e4"
    Tcon_Wild = "4.9e2"
    Ncon_Wild = "1e4"
    Nfinal_Wild = "1.5e4"
    N_Wild = "1.6e4" # for base only
    self_Wild0_rate = "0.1"
    self_Wild1_rate = "0.1"
    self_Wild2_rate = "0.1"

    # TV population
    Tshelf_TV = "3.2e3"
    N0_TV = "1.2e4"
    Nshelf_TV = N0_TV
    Ncon_TV = "1.8e3"
    Tcon_exp_TV = "1.3e3" # exp only
    Texp_TV = "1.3e3" # exp only
    Nexp_TV = "6e4" # exp only
    self_TV0_rate = "0.5"
    self_TV1_rate = self_TV0_rate
    self_TV2_rate = self_TV0_rate

    # Migration
    Tmig_WildTV = "1.8e3"
    Tmig_WildTV2 = "1.3e3"
    Tmig_TVWild = "1.3e3"
    Mig_WildTV = "1e-4"
    Mig_WildTV2 = "1e-4"
    Mig_TVWild = "1e-4"

# build the yaml files:
# generate file names using sys args
if template == True:
    file_name = str(model + "_" + complexity + "_" + ancient_exp + "_" + shelf + "_" + TV_exp + "_" + "TV_" + selfing + "_WildAnc_" + selfing_all + "_migepoch_" + str(mig_epoch) + "_template.yaml")
elif template == False:
    file_name = str(model + "_" + complexity + "_" + ancient_exp + "_" + shelf + "_" + TV_exp + "_" + "TV_" + selfing + "_WildAnc_" + selfing_all + "_migepoch_" + str(mig_epoch) + "_model.yaml")

# yaml header
model_description = """\
description: {0}
time_units: years
generation_time: 1
demes:
""".format(model + " + " + complexity + " + " + ancient_exp + " + " + shelf + " + " + TV_exp + " + TV " + selfing + " + WildAnc " + selfing_all + "mig_epoch" + str(mig_epoch))

# Ancestral population
if ancient_exp == "anc_exp":
    anc_epoch = """\
  - name: anc
    description: Equilibrium/root population
    epochs:
    - end_time: {0}
      start_size: {1}{6}
    - end_time: {2}
      end_size: {3}{7}
    - end_time: {4}
      end_size: {5}{8}""".format(T0_anc, N0_anc, T1_anc, N1_anc, Tfinal_anc, Nfinal_anc,
                                 "\n      selfing_rate: {0}".format(self_anc0_rate) if selfing_all == "self" else "",
                                 "\n      selfing_rate: {0}".format(self_anc1_rate) if selfing_all == "self" else "",
                                 "\n      selfing_rate: {0}".format(self_anc2_rate) if selfing_all == "self" else "")

elif ancient_exp == "anc_noexp":
    anc_epoch = """\
  - name: anc
    description: Equilibrium/root population
    epochs:
    - end_time: {0}
      start_size: {1}{4}
    - end_time: {2}
      end_size: {3}{5}""".format(T0_anc, N0_anc, Tfinal_anc, Nfinal_anc,
                                 "\n      selfing_rate: {0}".format(self_anc0_rate) if selfing_all == "self" else "",
                                 "\n      selfing_rate: {0}".format(self_anc1_rate) if selfing_all == "self" else "")

# Wild population
Wild = """
  - name: Wild
    description: Wild H. annuus
    ancestors: [anc]
    epochs:"""
if complexity == "base":
    Wildexp = """
    - start_size: {0}
      end_time: 0{1}""".format(N_Wild, "\n      selfing_rate: {0}".format(self_Wild0_rate) if selfing_all == "self" else "")
elif complexity == "hyper":
    Wildexp = """
    - end_time: {0}
      start_size: {1}
      end_size: {2}{6}
    - end_time: {3}
      end_size: {4}{7}
    - end_time: 0
      end_size: {5}{8}""".format(T0_Wild, N0_Wild, N0exp_Wild, Tcon_Wild, Ncon_Wild, Nfinal_Wild,
                                 "\n      selfing_rate: {0}".format(self_Wild0_rate) if selfing_all == "self" else "",
                                 "\n      selfing_rate: {0}".format(self_Wild1_rate) if selfing_all == "self" else "",
                                 "\n      selfing_rate: {0}".format(self_Wild2_rate) if selfing_all == "self" else "")

# TV population
TV = """
  - name: TV
    description: T . annuus traditional varieties 
    ancestors: [anc]
    epochs:"""
if TV_exp == "TV_noexp":
    # print("this could should not be running")
    if shelf == "noshelf":
        TV_shelf = """
    - end_time: 0
      start_size: {1}
      end_size: {2}{0}""".format("\n      selfing_rate: {0}".format(self_TV0_rate) if selfing == "self" else "", N0_TV, Ncon_TV)
    elif shelf == "shelf":
        # print("this could should not be running")
        TV_shelf = """
    - end_time: {2}
      start_size: {3}
      end_size: {4}{0}
    - end_time: 0
      end_size: {5}{1}""".format("\n      selfing_rate: {0}".format(self_TV0_rate) if selfing == "self" else "", 
                                 "\n      selfing_rate: {0}".format(self_TV1_rate) if selfing == "self" else "", Tshelf_TV, N0_TV, Nshelf_TV, Ncon_TV)
    TVexp = """"""
elif TV_exp == "TV_exp":
    if shelf == "noshelf":
        TV_shelf = """
    - end_time: {1}
      start_size: {2}
      end_size: {3}{0}""".format("\n      selfing_rate: {0}".format(self_TV0_rate) if selfing == "self" else "", Tcon_exp_TV, N0_TV, Ncon_TV)
    elif shelf == "shelf":
        TV_shelf = """
    - end_time: {2}
      start_size: {3}
      end_size: {4}{0}
    - end_time: {5}
      end_size: {6}{1}""".format("\n      selfing_rate: {0}".format(self_TV0_rate) if selfing == "self" else "", 
                                 "\n      selfing_rate: {0}".format(self_TV1_rate) if selfing == "self" else "", Tshelf_TV, N0_TV, Nshelf_TV, Texp_TV, Ncon_TV)
    TVexp = """
    - end_time: 0
      end_size: {1}{0}""".format(f"\n      selfing_rate: {self_TV1_rate if shelf == 'noshelf' else self_TV2_rate}" if selfing == "self" else "", Nexp_TV)

# Migration
if model == "no_mig":
    migration = """"""
elif model == "uni_mig":
    if mig_epoch == 1:
      migration = """
migrations:
  - {{source: Wild, dest: TV, rate: {Mig_WildTV}, start_time: {Tmig_WildTV}, end_time: 0}}""".format(Mig_WildTV=Mig_WildTV, Tmig_WildTV=Tmig_WildTV)
    if mig_epoch == 2:
      migration = """
migrations:
  - {{source: Wild, dest: TV, rate: {Mig_WildTV}, start_time: {Tmig_WildTV}, end_time: {Tmig_WildTV2}}}
  - {{source: Wild, dest: TV, rate: {Mig_WildTV2}, start_time: {Tmig_WildTV2}, end_time: 0}}""".format(Mig_WildTV=Mig_WildTV, Tmig_WildTV=Tmig_WildTV, Tmig_WildTV2=Tmig_WildTV2, Mig_WildTV2=Mig_WildTV2)

elif model == "bi_mig":
    if mig_epoch == 1:
      migration = """
migrations:
  - {{source: Wild, dest: TV, rate: {Mig_WildTV}, start_time: {Tmig_WildTV}, end_time: 0}}
  - {{source: TV, dest: Wild, rate: {Mig_TVWild}, start_time: {Tmig_TVWild}, end_time: 0}}""".format(Mig_WildTV=Mig_WildTV, Tmig_WildTV=Tmig_WildTV, Mig_TVWild=Mig_TVWild, Tmig_TVWild=Tmig_TVWild)
    if mig_epoch == 2:
      migration = """
migrations:
  - {{source: Wild, dest: TV, rate: {Mig_WildTV}, start_time: {Tmig_WildTV}, end_time: {Tmig_WildTV2}}}
  - {{source: Wild, dest: TV, rate: {Mig_WildTV2}, start_time: {Tmig_WildTV2}, end_time: 0}}
  - {{source: TV, dest: Wild, rate: {Mig_TVWild}, start_time: {Tmig_TVWild}, end_time: 0}}""".format(Mig_WildTV=Mig_WildTV, Tmig_WildTV=Tmig_WildTV, Tmig_WildTV2=Tmig_WildTV2, Mig_WildTV2=Mig_WildTV2, Mig_TVWild=Mig_TVWild, Tmig_TVWild=Tmig_TVWild)


# Check if files already exist and whether script has been instructed to overwrite. otherwise, writes it to specified location
if overwrite == False:
    print(f"File '{file_name}' already exists. Aborting model writing.")
    pass
else:
    print(f"File '{file_name}' does not exist or script instructed to overwrite. Creating it now.")
    with open("{0}/{1}/{2}".format(wd, template_wd if template == True else model_wd, file_name), 'w') as file:
        file.write(model_description)
        file.write(anc_epoch)
        file.write(TV)
        file.write(TV_shelf)
        file.write(TVexp)
        file.write(Wild)
        file.write(Wildexp)
        file.write(migration)
