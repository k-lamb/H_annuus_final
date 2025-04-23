
import os
import sys

# savio
wd = "/global/scratch/users/kericlamb/Hannuus_moments3/code/moments_scripts/models"
model_wd = "model_options" # where to save models nested within wd

# home system
# wd = "/Users/kericlamb/Documents/Work MacBook/Research/paper_code/H_annuus_demography/Hannuus_moments3_og/code/moments_scripts/models/scribe_ext" # upper level directory

sys.path.append(wd)
from options_bounds_config_admix import *

# defining input parameters for creating model files and their templates
model = sys.argv[1] # bi_mig uni_mig or no_mig
complexity = sys.argv[2] # base or hyper
ancient_exp = sys.argv[3] # anc_exp or anc_noexp
shelf = sys.argv[4] # shelf or noshelf
TV_exp = sys.argv[5] # TV_exp or TV_noexp
selfing = sys.argv[6] # self or outcross for TV
overwrite = True # True or False (whether to overwrite existing model & template files)
selfing_all = sys.argv[7] # self or outcross for Wild/Anc
pulse = sys.argv[8] # pulse or none

# define model parameters:
# ancestral population
T0_anc_param = """
- name: {T0_anc}
  description: Time of ancestral contraction
  values:
  - demes:
      anc:
        epochs:
          0: end_time
  upper_bound: {T0_anc_upper}
  lower_bound: {T0_anc_lower}""".format(T0_anc=T0_anc, T0_anc_upper=T0_anc_upper, T0_anc_lower=T0_anc_lower)
N0_anc_param = """
- name: {N0_anc}
  description: Ancestral effective population size pre-contraction
  values:
  - demes:
      anc:
        epochs:
          0: start_size
  upper_bound: {N0_anc_upper}
  lower_bound: {N0_anc_lower}""".format(N0_anc=N0_anc, N0_anc_upper=N0_anc_upper, N0_anc_lower=N0_anc_lower)
T1_anc_param = """
- name: {T1_anc}
  description: Time of ancestral expansion post-contraction
  values:
  - demes:
      anc:
        epochs:
          1: end_time
  upper_bound: {T1_anc_upper}
  lower_bound: {T1_anc_lower}""".format(T1_anc=T1_anc, T1_anc_upper=T1_anc_upper, T1_anc_lower=T1_anc_lower)
N1_anc_param = """
- name: {N1_anc}
  description: Time of ancestral expansion post-contraction
  values:
  - demes:
      anc:
        epochs:
          1: end_size
  upper_bound: {N1_anc_upper}
  lower_bound: {N1_anc_lower}""".format(N1_anc=N1_anc, N1_anc_upper=N1_anc_upper, N1_anc_lower=N1_anc_lower)
Tfinal_anc_param = """
- name: {Tfinal_anc}
  description: Time of split between TV and Wild
  values:
  - demes:
      anc:
        epochs:
          {epoch}: end_time
  upper_bound: {Tfinal_anc_upper}
  lower_bound: {Tfinal_anc_lower}""".format(Tfinal_anc=Tfinal_anc, Tfinal_anc_upper=Tfinal_anc_upper, Tfinal_anc_lower=Tfinal_anc_lower,
                                            epoch="2" if ancient_exp == "anc_exp" else "1")
Nfinal_anc_param = """
- name: {Nfinal_anc}
  description: Final size of ancestral population
  values:
  - demes:
      anc:
        epochs:
          {epoch}: end_size
  upper_bound: {Nfinal_anc_upper}
  lower_bound: {Nfinal_anc_lower}""".format(Nfinal_anc=Nfinal_anc, Nfinal_anc_upper=Nfinal_anc_upper, Nfinal_anc_lower=Nfinal_anc_lower,
                                            epoch="2" if ancient_exp == "anc_exp" else "1")
self_anc0_rate_param = """
- name: {self_anc0_rate}
  description: selfing rate for Anc
  values:
  - demes:
      anc:
        epochs:
          0: selfing_rate
  upper_bound: {self_anc0_rate_upper}
  lower_bound: {self_anc0_rate_lower}""".format(self_anc0_rate=self_anc0_rate, self_anc0_rate_upper=self_anc0_rate_upper, self_anc0_rate_lower=self_anc0_rate_lower)
self_anc1_rate_param = """
- name: {self_anc1_rate}
  description: selfing rate for Anc
  values:
  - demes:
      anc:
        epochs:
          1: selfing_rate
  upper_bound: {self_anc1_rate_upper}
  lower_bound: {self_anc1_rate_lower}""".format(self_anc1_rate=self_anc1_rate, self_anc1_rate_upper=self_anc1_rate_upper, self_anc1_rate_lower=self_anc1_rate_lower)
self_anc2_rate_param = """
- name: {self_anc2_rate}
  description: selfing rate for Anc
  values:
  - demes:
      anc:
        epochs:
          2: selfing_rate
  upper_bound: {self_anc2_rate_upper}
  lower_bound: {self_anc2_rate_lower}""".format(self_anc2_rate=self_anc2_rate, self_anc2_rate_upper=self_anc2_rate_upper, self_anc2_rate_lower=self_anc2_rate_lower)

# Wild population
N_Wild_param = """
- name: {0}
  description: constant Wild population size
  values:
  - demes:
      Wild:
        epochs:
          0: start_size
  upper_bound: {1}
  lower_bound: {2}""".format(N_Wild, N_Wild_upper, N_Wild_lower) # base parameter
T0_Wild_param = """
- name: {T0_Wild}
  description: time when expansion ceases and contraction begins
  values:
  - demes:
      Wild:
        epochs:
          0: end_time
  upper_bound: {T0_Wild_upper}
  lower_bound: {T0_Wild_lower}""".format(T0_Wild=T0_Wild, T0_Wild_upper=T0_Wild_upper, T0_Wild_lower=T0_Wild_lower)
N0_Wild_param = """
- name: {N0_Wild}
  description: pre-expansion size
  values:
  - demes:
      Wild:
        epochs:
          0: start_size
  upper_bound: {N0_Wild_upper}
  lower_bound: {N0_Wild_lower}""".format(N0_Wild=N0_Wild, N0_Wild_upper=N0_Wild_upper, N0_Wild_lower=N0_Wild_lower)
N0exp_Wild_param = """
- name: {N0exp_Wild}
  description: expanded size
  values:
  - demes:
      Wild:
        epochs:
          0: end_size
  upper_bound: {N0exp_Wild_upper}
  lower_bound: {N0exp_Wild_lower}""".format(N0exp_Wild=N0exp_Wild, N0exp_Wild_upper=N0exp_Wild_upper, N0exp_Wild_lower=N0exp_Wild_lower)
Tcon_Wild_param = """
- name: {Tcon_Wild}
  description: time contraction ends and expansion begins again
  values:
  - demes:
      Wild:
        epochs:
          1: end_time
  upper_bound: {Tcon_Wild_upper}
  lower_bound: {Tcon_Wild_lower}""".format(Tcon_Wild=Tcon_Wild, Tcon_Wild_upper=Tcon_Wild_upper, Tcon_Wild_lower=Tcon_Wild_lower)
Ncon_Wild_param = """
- name: {Ncon_Wild}
  description: contracted size
  values:
  - demes:
      Wild:
        epochs:
          1: end_size
  upper_bound: {Ncon_Wild_upper}
  lower_bound: {Ncon_Wild_lower}""".format(Ncon_Wild=Ncon_Wild, Ncon_Wild_upper=Ncon_Wild_upper, Ncon_Wild_lower=Ncon_Wild_lower)
Nfinal_Wild_param = """
- name: {Nfinal_Wild}
  description: contracted size
  values:
  - demes:
      Wild:
        epochs:
          2: end_size
  upper_bound: {Nfinal_Wild_upper}
  lower_bound: {Nfinal_Wild_lower}""".format(Nfinal_Wild=Nfinal_Wild, Nfinal_Wild_upper=Nfinal_Wild_upper, Nfinal_Wild_lower=Nfinal_Wild_lower)
self_Wild0_rate_param = """
- name: {self_Wild0_rate}
  description: selfing rate for Wild
  values:
  - demes:
      Wild:
        epochs:
          0: selfing_rate
  upper_bound: {self_Wild0_rate_upper}
  lower_bound: {self_Wild0_rate_lower}""".format(self_Wild0_rate=self_Wild0_rate, self_Wild0_rate_upper=self_Wild0_rate_upper, self_Wild0_rate_lower=self_Wild0_rate_lower)
self_Wild1_rate_param = """
- name: {self_Wild1_rate}
  description: selfing rate for Wild
  values:
  - demes:
      Wild:
        epochs:
          1: selfing_rate
  upper_bound: {self_Wild1_rate_upper}
  lower_bound: {self_Wild1_rate_lower}""".format(self_Wild1_rate=self_Wild1_rate, self_Wild1_rate_upper=self_Wild1_rate_upper, self_Wild1_rate_lower=self_Wild1_rate_lower)
self_Wild2_rate_param = """
- name: {self_Wild2_rate}
  description: selfing rate for Wild
  values:
  - demes:
      Wild:
        epochs:
          2: selfing_rate
  upper_bound: {self_Wild2_rate_upper}
  lower_bound: {self_Wild2_rate_lower}""".format(self_Wild2_rate=self_Wild2_rate, self_Wild2_rate_upper=self_Wild2_rate_upper, self_Wild2_rate_lower=self_Wild2_rate_lower)

# TV population
N0_TV_param = """
- name: {N0_TV}
  description: pre-contraction (a.k.a. starting) size
  values:
  - demes:
      TV:
        epochs:
          0: start_size
  upper_bound: {N0_TV_upper}
  lower_bound: {N0_TV_lower}""".format(N0_TV=N0_TV, N0_TV_upper=N0_TV_upper, N0_TV_lower=N0_TV_lower)
Ncon_TV_param = """
- name: {Ncon_TV}
  description: contraction size
  values:
  - demes:
      TV:
        epochs:
          {{0}}: end_size
  upper_bound: {Ncon_TV_upper}
  lower_bound: {Ncon_TV_lower}""".format(Ncon_TV=Ncon_TV, Ncon_TV_upper=Ncon_TV_upper, Ncon_TV_lower=Ncon_TV_lower)
self_TV0_rate_param = """
- name: {self_TV0_rate}
  description: selfing rate for TV
  values:
  - demes:
      TV:
        epochs:
          0: selfing_rate
  upper_bound: {self_TV0_rate_upper}
  lower_bound: {self_TV0_rate_lower}""".format(self_TV0_rate=self_TV0_rate, self_TV0_rate_upper=self_TV0_rate_upper, self_TV0_rate_lower=self_TV0_rate_lower)
Tshelf_TV_param = """
- name: {Tshelf_TV}
  description: Time when steady-state ends
  values:
  - demes:
      TV:
        epochs:
          0: end_time
  upper_bound: {Tshelf_TV_upper}
  lower_bound: {Tshelf_TV_lower}""".format(Tshelf_TV=Tshelf_TV, Tshelf_TV_upper=Tshelf_TV_upper, Tshelf_TV_lower=Tshelf_TV_lower)
Nshelf_TV_param = """
- name: {Nshelf_TV}
  description: pre-contraction size (end of steady-state)
  values:
  - demes:
      TV:
        epochs:
          0: end_size
  upper_bound: {Nshelf_TV_upper}
  lower_bound: {Nshelf_TV_lower}""".format(Nshelf_TV=Nshelf_TV, Nshelf_TV_upper=Nshelf_TV_upper, Nshelf_TV_lower=Nshelf_TV_lower)
self_TV1_rate_param = """
- name: {self_TV1_rate}
  description: selfing rate for TV
  values:
  - demes:
      TV:
        epochs:
          1: selfing_rate
  upper_bound: {self_TV1_rate_upper}
  lower_bound: {self_TV1_rate_lower}""".format(self_TV1_rate=self_TV1_rate, self_TV1_rate_upper=self_TV1_rate_upper, self_TV1_rate_lower=self_TV1_rate_lower)
Tcon_exp_TV_param = """
- name: {Tcon_exp_TV}
  description: time when contraction ceases and expansion begins
  values:
  - demes:
      TV:
        epochs:
          0: end_time
  upper_bound: {Tcon_exp_TV_upper}
  lower_bound: {Tcon_exp_TV_lower}""".format(Tcon_exp_TV=Tcon_exp_TV, Tcon_exp_TV_upper=Tcon_exp_TV_upper, Tcon_exp_TV_lower=Tcon_exp_TV_lower)
Texp_TV_param = """
- name: {Texp_TV}
  description: time when expansion ends and con1 begins
  values:
  - demes:
      TV:
        epochs:
          1: end_time
  upper_bound: {Texp_TV_upper}
  lower_bound: {Texp_TV_lower}""".format(Texp_TV=Texp_TV, Texp_TV_upper=Texp_TV_upper, Texp_TV_lower=Texp_TV_lower)
Nexp_TV_param = """
- name: {Nexp_TV}
  description: expansion size
  values:
  - demes:
      TV:
        epochs:
          {{0}}: end_size
  upper_bound: {Nexp_TV_upper}
  lower_bound: {Nexp_TV_lower}""".format(Nexp_TV=Nexp_TV, Nexp_TV_upper=Nexp_TV_upper, Nexp_TV_lower=Nexp_TV_lower)
self_TV2_rate_param = """
- name: {self_TV2_rate}
  description: selfing rate for TV
  values:
  - demes:
      TV:
        epochs:
          2: selfing_rate
  upper_bound: {self_TV2_rate_upper}
  lower_bound: {self_TV2_rate_lower}""".format(self_TV2_rate=self_TV2_rate, self_TV2_rate_upper=self_TV2_rate_upper, self_TV2_rate_lower=self_TV2_rate_lower)
# Migration
Mig_WildTV_param = """
- name: {Mig_WildTV}
  description: migration rate between TV and Wild
  values:
  - migrations:
      0: rate
  upper_bound: {Mig_WildTV_upper}
  lower_bound: {Mig_WildTV_lower}""".format(Mig_WildTV=Mig_WildTV, Mig_WildTV_upper=Mig_WildTV_upper, Mig_WildTV_lower=Mig_WildTV_lower)
Mig_TVWild_param = """
- name: {Mig_TVWild}
  description: migration rate between Wild and TV
  values:
  - migrations:
      0: rate
  upper_bound: {Mig_TVWild_upper}
  lower_bound: {Mig_TVWild_lower}""".format(Mig_TVWild=Mig_TVWild, Mig_TVWild_upper=Mig_TVWild_upper, Mig_TVWild_lower=Mig_TVWild_lower)
Tmig_WildTV_param = """
- name: {Tmig_WildTV}
  description: migration time between TV and Wild
  values:
  - migrations:
      0: start_time
  upper_bound: {Tmig_WildTV_upper}
  lower_bound: {Tmig_WildTV_lower}""".format(Tmig_WildTV=Tmig_WildTV, Tmig_WildTV_upper=Tmig_WildTV_upper, Tmig_WildTV_lower=Tmig_WildTV_lower)
Tmig_TVWild_param = """
- name: {Tmig_TVWild}
  description: migration time between TV and Wild
  values:
  - migrations:
      0: start_time
  upper_bound: {Tmig_TVWild_upper}
  lower_bound: {Tmig_TVWild_lower}""".format(Tmig_TVWild=Tmig_TVWild, Tmig_TVWild_upper=Tmig_TVWild_upper, Tmig_TVWild_lower=Tmig_TVWild_lower)

# Pulse admixture
pulse_WildTV_param = """
- name: {pulse_WildTV}
  description: proportion pulse admixture
  values:
  - pulses:
      0: proportions
  upper_bound: {pulse_WildTV_upper}
  lower_bound: {pulse_WildTV_lower}""".format(pulse_WildTV=pulse_WildTV, pulse_WildTV_upper=pulse_WildTV_upper, pulse_WildTV_lower=pulse_WildTV_lower)
Tpulse_WildTV_param = """
- name: {Tpulse_WildTV}
  description: proportion pulse admixture
  values:
  - pulses:
      0: time
  upper_bound: {Tpulse_WildTV_upper}
  lower_bound: {Tpulse_WildTV_lower}""".format(Tpulse_WildTV=Tpulse_WildTV, Tpulse_WildTV_upper=Tpulse_WildTV_upper, Tpulse_WildTV_lower=Tpulse_WildTV_lower)


# define constraints:
# ancestral population constraints
T1_anc_constraint = """
- params: [{T0_anc}, {T1_anc}]
  constraint: greater_than""".format(T0_anc=T0_anc, T1_anc=T1_anc)
Tfinal_anc_constraint = """
- params: [{T_anc_prior}, {Tfinal_anc}]
  constraint: greater_than""".format(T_anc_prior = T1_anc if ancient_exp == "anc_exp" else T0_anc, Tfinal_anc=Tfinal_anc)
N0_anc_exp_constraint = """
- params: [{N0_anc}, {N1_anc}]
  constraint: greater_than""".format(N0_anc = N0_anc, N1_anc = N1_anc)
N1_anc_exp_constraint = """
- params: [{Nfinal_anc}, {N1_anc}]
  constraint: greater_than""".format(Nfinal_anc = Nfinal_anc, N1_anc = N1_anc)
N0_anc_noexp_constraint = """
- params: [{N0_anc}, {Nfinal_anc}]
  constraint: greater_than""".format(N0_anc = N0_anc, Nfinal_anc = Nfinal_anc)

# Wild populaiton constraints
T0_Wild_constraint = """
- params: [{Tfinal_anc}, {T0_Wild}]
  constraint: greater_than""".format(Tfinal_anc=Tfinal_anc, T0_Wild=T0_Wild) 
Tcon_Wild_constraint = """
- params: [{T0_Wild}, {Tcon_Wild}]
  constraint: greater_than""".format(T0_Wild=T0_Wild, Tcon_Wild=Tcon_Wild)

# TV population constraints
Tshelf_TV_constraint = """
- params: [{Tfinal_anc}, {Tshelf_TV}]
  constraint: greater_than""".format(Tfinal_anc=Tfinal_anc, Tshelf_TV=Tshelf_TV)
Tcon_exp_TV_constraint = """
- params: [{Tfinal_anc}, {Tcon_exp_TV}]
  constraint: greater_than""".format(Tfinal_anc=Tfinal_anc, Tcon_exp_TV=Tcon_exp_TV)
Texp_TV_constraint = """
- params: [{Tshelf_TV}, {Texp_TV}]
  constraint: greater_than""".format(Tshelf_TV=Tshelf_TV, Texp_TV=Texp_TV)

# migration constriants
Tmig_TVWild_constraint = """
- params: [{Tfinal_anc}, {Tmig_TVWild}]
  constraint: greater_than""".format(Tfinal_anc=Tfinal_anc, Tmig_TVWild=Tmig_TVWild)
Tmig_WildTV_constraint = """
- params: [{Tfinal_anc}, {Tmig_WildTV}]
  constraint: greater_than""".format(Tfinal_anc=Tfinal_anc, Tmig_WildTV=Tmig_WildTV)

# admixture constraints
Tpulse_admix_constraint = """
- params: [{Tfinal_anc}, {Tpulse_WildTV}]
  constraint: greater_than""".format(Tfinal_anc=Tfinal_anc, Tpulse_WildTV=Tpulse_WildTV)

# compose options file:
# headers
options_header = """\
parameters:"""
constraints_header = """
constraints:"""

# ancestral population options
anc_epoch0 = "{0}{1}{2}".format(T0_anc_param, N0_anc_param, self_anc0_rate_param if selfing_all == "self" else "")
if ancient_exp == "anc_exp":
    anc_epoch1 = "{0}{1}{2}".format(T1_anc_param, N1_anc_param, self_anc1_rate_param if selfing_all == "self" else "")
    anc_epoch2 = "{0}{1}{2}".format(Tfinal_anc_param, Nfinal_anc_param, self_anc2_rate_param if selfing_all == "self" else "")
    anc_constraints = T1_anc_constraint + Tfinal_anc_constraint + N0_anc_exp_constraint + N1_anc_exp_constraint
elif ancient_exp == "anc_noexp":
    anc_epoch1 = ""
    anc_epoch2 = "{0}{1}{2}".format(Tfinal_anc_param, Nfinal_anc_param, self_anc1_rate_param if selfing_all == "self" else "")
    anc_constraints = Tfinal_anc_constraint + N0_anc_noexp_constraint
anc_params = anc_epoch0 + anc_epoch1 + anc_epoch2

# wild population options
if complexity == "base":
    Wild_params = "{0}{1}".format(N_Wild_param, self_Wild0_rate_param if selfing_all == "self" else "")
    Wild_constraints = ""
elif complexity == "hyper":
    Wild_params = "{0}{1}{2}{3}{4}{5}{6}{7}{8}".format(T0_Wild_param, N0_Wild_param, N0exp_Wild_param, Tcon_Wild_param, Ncon_Wild_param, Nfinal_Wild_param,
                                                       self_Wild0_rate_param if selfing_all == "self" else "", self_Wild1_rate_param if selfing_all == "self" else "",
                                                       self_Wild2_rate_param if selfing_all == "self" else "")
    Wild_constraints = T0_Wild_constraint + Tcon_Wild_constraint

# TV population options
if TV_exp == "TV_noexp":
    if shelf == "noshelf":
        TV_params = "{0}{1}{2}".format(N0_TV_param, Ncon_TV_param.format("0"), self_TV0_rate_param if selfing == "self" else "") # epoch 0
        TV_constraints = ""
    elif shelf == "shelf":
        TV_params = "{0}{1}{2}{3}".format(Tshelf_TV_param, N0_TV_param, Nshelf_TV_param, self_TV0_rate_param if selfing == "self" else "") # epoch 0
        TV_params = "{0}{1}{2}".format(TV_params, Ncon_TV_param.format("1"), self_TV1_rate_param if selfing == "self" else "")  # epoch 1
        TV_constraints = Tshelf_TV_constraint
elif TV_exp == "TV_exp":
    if shelf == "noshelf":
        TV_params = "{0}{1}{2}{3}".format(Tcon_exp_TV_param, N0_TV_param, Ncon_TV_param.format("0"), self_TV0_rate_param if selfing == "self" else "") # epoch 0
        TV_params = "{0}{1}{2}".format(TV_params, Nexp_TV_param.format("1"), self_TV1_rate_param if selfing == "self" else "") # epoch 1
        TV_constraints = Tcon_exp_TV_constraint
    elif shelf == "shelf":
        TV_params = "{0}{1}{2}{3}".format(Tshelf_TV_param, N0_TV_param, Nshelf_TV_param, self_TV0_rate_param if selfing == "self" else "") # epoch 0
        TV_params = "{0}{1}{2}{3}".format(TV_params, Texp_TV_param, Ncon_TV_param.format("1"), self_TV1_rate_param if selfing == "self" else "") # epoch 1
        TV_params = "{0}{1}{2}".format(TV_params, Nexp_TV_param.format("2"), self_TV2_rate_param if selfing == "self" else "") # epoch 2
        TV_constraints = Tshelf_TV_constraint + Texp_TV_constraint

# migration options
if model == "no_mig":
    mig_params = ""
    mig_constraints = ""
elif model == "uni_mig":
    mig_params = Tmig_WildTV_param + Mig_WildTV_param
    mig_constraints = Tmig_WildTV_constraint
elif model == "bi_mig":
    mig_params = Tmig_WildTV_param + Tmig_TVWild_param + Mig_WildTV_param + Mig_TVWild_param
    mig_constraints = Tmig_WildTV_constraint + Tmig_TVWild_constraint

# admixture options
if pulse == "none":
    pulse_params = ""
    pulse_constraints = ""
elif pulse == "pulse":
    pulse_params = Tpulse_WildTV_param
    pulse_constraints = Tpulse_admix_constraint

# print options to file:
file_name = str(model + "_" + complexity + "_" + ancient_exp + "_" + shelf + "_" + TV_exp + "_" + "TV_" + selfing + "_WildAnc_" + selfing_all + "_admix_" + pulse + "_options.yaml")

if os.path.exists("{0}/{1}/{2}".format(wd, model_wd, file_name)) and overwrite == False:
    print(f"File '{file_name}' already exists. Aborting model writing.")
    pass
else:
    print(f"File '{file_name}' does not exist or script instructed to overwrite. Creating it now.")
    with open("{0}/{1}/{2}".format(wd, model_wd, file_name), 'w') as file:
        file.write(options_header)
        file.write(anc_params)
        file.write(TV_params)
        file.write(Wild_params)
        file.write(mig_params)
        file.write(pulse_params)
        file.write(constraints_header)
        file.write(anc_constraints)
        file.write(TV_constraints)
        file.write(Wild_constraints)
        file.write(mig_constraints)
        file.write(pulse_constraints)
