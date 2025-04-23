# Define parameter names and bounds for model_scribe_options.py 
# ancestral population
T0_anc = "T0_anc"
T0_anc_upper = "100000000" # was 400,000
T0_anc_lower = "10"

N0_anc = "N0_anc"
N0_anc_upper = "100000000"
N0_anc_lower = "10"

T1_anc = "T1_anc"
T1_anc_upper = "100000000" # was 11,400 then 15,000 then 20,000
T1_anc_lower = "10"

N1_anc = "N1_anc"
N1_anc_upper = "100000000" # was 12,450
N1_anc_lower = "10" # was 4,150

Tfinal_anc = "Tfinal_anc"
Tfinal_anc_upper = "5500" # was 10,000. beware fixing with too small of a difference (5301-5299) will prevent perturbation
Tfinal_anc_lower = "5100" # was 4,000

Nfinal_anc = "Nfinal_anc"
Nfinal_anc_upper = "100000000" # was 18,300 then 25,000 then 35,000 then 60,000
Nfinal_anc_lower = "10"

self_anc0_rate = "self_anc0_rate" 
self_anc0_rate_upper = "1"
self_anc0_rate_lower= "0.01"

self_anc1_rate = "self_anc1_rate" 
self_anc1_rate_upper = "1"
self_anc1_rate_lower = "0.01"

self_anc2_rate = "self_anc2_rate"
self_anc2_rate_upper = "1"
self_anc2_rate_lower = "0.01"

# Wild population
T0_Wild = "T0_Wild"
T0_Wild_upper = Tfinal_anc_upper # was 4,800
T0_Wild_lower = "10" # was 1,600

N0_Wild = "N0_Wild"
N0_Wild_upper = "100000000" # was 18,300 then 25,000
N0_Wild_lower = "10"

N0exp_Wild = "N0exp_Wild"
N0exp_Wild_upper = "100000000" # was 39,700 then 70,000
N0exp_Wild_lower = "10"

Tcon_Wild = "Tcon_Wild"
Tcon_Wild_upper = "100000000" # was 750
Tcon_Wild_lower = "10" # was 250

Ncon_Wild = "Ncon_Wild"
Ncon_Wild_upper = "100000000" # was 15,000 then 25,000
Ncon_Wild_lower = "10"

Nfinal_Wild = "Nfinal_Wild"
Nfinal_Wild_upper = "100000000" # was 22,500
Nfinal_Wild_lower = "10"

N_Wild = "N_Wild" # base only
N_Wild_upper = "100000000" # base only
N_Wild_lower = "10" # base only

self_Wild0_rate = "self_Wild0_rate" 
self_Wild0_rate_upper = "1"
self_Wild0_rate_lower= "0.01"

self_Wild1_rate = "self_Wild1_rate" 
self_Wild1_rate_upper = "1"
self_Wild1_rate_lower = "0.01"

self_Wild2_rate = "self_Wild2_rate"
self_Wild2_rate_upper = "1"
self_Wild2_rate_lower = "0.01"

# TV population
Tshelf_TV = "Tshelf_TV"
Tshelf_TV_upper = "100000000"
Tshelf_TV_lower = "10"

N0_TV = "N0_TV"
N0_TV_upper = "100000000" # was 18,300 then 25,000
N0_TV_lower = "10" # was 6,100

Nshelf_TV = "Nshelf_TV"
Nshelf_TV_upper = N0_TV_upper
Nshelf_TV_lower = N0_TV_lower

Ncon_TV = "Ncon_TV"
Ncon_TV_upper = "100000000" # was 2,700
Ncon_TV_lower = "10" # was 900

Tcon_exp_TV = "Tcon_exp_TV" # exp only
Tcon_exp_TV_upper = "100000000" # exp only
Tcon_exp_TV_lower = "1" # exp only

Texp_TV = "Texp_TV" # exp only
Texp_TV_upper = "100000000" # exp only
Texp_TV_lower = "1" # exp only

Nexp_TV = "Nexp_TV" # exp only
Nexp_TV_upper = "100000000" # exp only
Nexp_TV_lower = "10" # exp only

self_TV0_rate = "self_TV0_rate" 
self_TV0_rate_upper = "1"
self_TV0_rate_lower= "0.01"

self_TV1_rate = "self_TV1_rate" 
self_TV1_rate_upper = "1"
self_TV1_rate_lower = "0.01"

self_TV2_rate = "self_TV2_rate"
self_TV2_rate_upper = "1"
self_TV2_rate_lower = "0.01"

# migration
Tmig_WildTV = "Tmig_WildTV"
Tmig_WildTV_upper = Tfinal_anc_upper
Tmig_WildTV_lower = "10"

Tmig_TVWild = "Tmig_TVWild"
Tmig_TVWild_upper = Tfinal_anc_upper
Tmig_TVWild_lower = "10"

Mig_WildTV = "Mig_WildTV"
Mig_WildTV_upper = "1"
Mig_WildTV_lower = "1e-10"

Mig_TVWild = "Mig_TVWild"
Mig_TVWild_upper = "1"
Mig_TVWild_lower = "1e-10"

# pulse of admixture
pulse_WildTV = "pulse_WildTV"
pulse_WildTV_upper = "1"
pulse_WildTV_lower = "1e-5"

Tpulse_WildTV = "Tpulse_WildTV"
Tpulse_WildTV_upper = "100000"
Tpulse_WildTV_lower = "1"
