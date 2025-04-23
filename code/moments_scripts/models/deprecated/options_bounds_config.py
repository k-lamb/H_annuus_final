# Define parameter names and bounds for model_scribe_options.py
# ancestral population
T0_anc = "T0_anc"
T0_anc_upper = "600000" # was 4e5
T0_anc_lower = "50000"

N0_anc = "N0_anc"
N0_anc_upper = "150000"
N0_anc_lower = "10000"

T1_anc = "T1_anc"
T1_anc_upper = "11400"
T1_anc_lower = "3800"

N1_anc = "N1_anc"
N1_anc_upper = "12450"
N1_anc_lower = "4150"

Tfinal_anc = "Tfinal_anc"
Tfinal_anc_upper = "8000" # was 1e4
Tfinal_anc_lower = "4000"

Nfinal_anc = "Nfinal_anc"
Nfinal_anc_upper = "25000" # was 18300
Nfinal_anc_lower = "6100"

# Wild population
T0_Wild = "T0_Wild"
T0_Wild_upper = "4800"
T0_Wild_lower = "600" # was 1600

N0_Wild = "N0_Wild"
N0_Wild_upper = "23000" # was 18300
N0_Wild_lower = "6100"

N0exp_Wild = "N0exp_Wild"
N0exp_Wild_upper = "60000" #was 39700
N0exp_Wild_lower = "13200"

Tcon_Wild = "Tcon_Wild"
Tcon_Wild_upper = "750"
Tcon_Wild_lower = "250"

Ncon_Wild = "Ncon_Wild"
Ncon_Wild_upper = "15000"
Ncon_Wild_lower = "5000"

Nfinal_Wild = "Nfinal_Wild"
Nfinal_Wild_upper = "22500"
Nfinal_Wild_lower = "7500"

N_Wild = "N_Wild" # base only
N_Wild_upper = "50000" # base only
N_Wild_lower = "8000" # base only

# TV population
Tshelf_TV = "Tshelf_TV"
Tshelf_TV_upper = "8000" # was 4800
Tshelf_TV_lower = "1600"

N0_TV = "N0_TV"
N0_TV_upper = "18300"
N0_TV_lower = "1000" # was 6100

Nshelf_TV = "Nshelf_TV"
Nshelf_TV_upper = N0_TV_upper
Nshelf_TV_lower = N0_TV_lower

Ncon_TV = "Ncon_TV"
Ncon_TV_upper = "5000" # was 2700
Ncon_TV_lower = "200" # was 900

Tcon_exp_TV = "Tcon_exp_TV" # exp only
Tcon_exp_TV_upper = "4800" # exp only
Tcon_exp_TV_lower = "1" # exp only

Texp_TV = "Texp_TV" # exp only
Texp_TV_upper = "3000" # exp only
Texp_TV_lower = "1" # exp only

Nexp_TV = "Nexp_TV" # exp only
Nexp_TV_upper = "110000" # exp only # was 89400
Nexp_TV_lower = "29800" # exp only

self0_rate = "self0_rate" 
self0_rate_upper = "1"
self0_rate_lower= "0.01"

self1_rate = "self1_rate" 
self1_rate_upper = "1"
self1_rate_lower = "0.01"

self2_rate = "self2_rate"
self2_rate_upper = "1"
self2_rate_lower = "0.01"

# migration
Tmig_WildTV = "Tmig_WildTV"
Tmig_WildTV_upper = Tfinal_anc_upper
Tmig_WildTV_lower = "300"

Tmig_TVWild = "Tmig_TVWild"
Tmig_TVWild_upper = Tfinal_anc_upper
Tmig_TVWild_lower = "300"

Mig_WildTV = "Mig_WildTV"
Mig_WildTV_upper = "1"
Mig_WildTV_lower = "1e-10"

Mig_TVWild = "Mig_TVWild"
Mig_TVWild_upper = "1"
Mig_TVWild_lower = "1e-10"
