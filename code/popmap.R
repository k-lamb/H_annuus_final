#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE) 

# derive pop map from classifications in P.S. dissertation Table 1

library(dplyr)

metadat <- read.csv("/global/scratch/users/kericlamb/Hannuus_moments3/data/pop_metadata.csv")

# checks if pops exists and if not, generates a vcf from the default VCF
if (exists("pops") == FALSE) {
  library(vcfR)
  vcf <- read.vcfR(sprintf("/global/scratch/users/kericlamb/Hannuus_moments3/VCFs/%s_filter.vcf", as.character(args[1])))
  pops <- colnames(vcf@gt)[-1]
  pops <- data.frame(Specimen=pops)
}

pops$og_order <- rownames(pops) %>% as.numeric()
popdat <- merge(metadat, pops, by="Specimen")
popdat <- popdat %>% 
  group_by(Specimen) %>% 
  slice_head(n=1) %>% # why are there multiple per specimen?
  arrange(og_order) %>% 
  dplyr::select(Specimen, Type, og_order)

# missing 71,72,74 (Hopi_* ~ all TV variants)... reinsert
hopi_ <- data.frame(Specimen=c("Hopi_mapping_NEW", "Hopi_dye_NEW", "Hopi_real_NEW"), Type=rep("TV", 3), og_order=c(71,72,74))

popdat <- rbind(popdat, hopi_)
popdat <- popdat %>% 
  arrange(og_order) %>% 
  dplyr::select(Specimen, Type) %>% 
  ungroup() %>% 
  as.data.frame()

write.table(popdat, "/global/scratch/users/kericlamb/Hannuus_moments3/data/popmap.txt", sep="\t", row.names = F, col.names = F, quote=F)
print("popmap exported to ./data/popmap.txt")

