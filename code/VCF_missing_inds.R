#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)

# install.packages("vcfR", lib='/global/scratch/users/yourusername/R')
library(vcfR)

# setwd("global/scratch/users/kericlamb/Hannuus_moments")
vcf <- read.vcfR(sprintf("/global/scratch/users/kericlamb/Hannuus_moments3/VCFs/%s.vcf", as.character(args[1])))

gt <- vcf@gt
ind.miss <- colSums(is.na(gt))/dim(gt)[1] # missingness by individual
ind.miss <- data.frame(ind_miss=ind.miss[-1]) # remove first row that's just the format
ind.miss <- data.frame(ind=rownames(ind.miss), miss=ind.miss$ind_miss)

gt.miss <- rowSums(is.na(gt))/dim(gt)[2]
gt.miss <- as.data.frame(gt.miss) # gt.missingness is limited to 0.1... good to see. easySFS dimension issue might be due to individual missingness

write.table(ind.miss, "/global/scratch/users/kericlamb/Hannuus_moments3/data/ind_missingness.txt", sep="\t", quote=F, row.names=F)

missing <- as.numeric(args[2]) # user-defined missing threshold
ind.miss.filter <- subset(ind.miss, miss <=  missing)

write.table(ind.miss.filter, "/global/scratch/users/kericlamb/Hannuus_moments3/data/ind_missing_threshold.txt", sep="\t", quote=F, row.names=F, col.names=F)
