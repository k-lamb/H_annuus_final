#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE) 

# script requires 3 inputs: 
# threshold filter for determining segregating sites (1-alpha)
# name of vcf file
# number of iterations to run Moments 

### metadata prep for Moments runs ###
# want to generate a df with columns for: iterations, pair (pair name), pop1, pop2, proj1, proj2

library(dplyr)

proj <- read.csv("/global/scratch/users/kericlamb/Hannuus_moments3/data/easySFS_output_processed.csv")

# want to select highest projection possible while maximizing segregating site number using ± a threshold determiner of projections to retain
temp <- proj %>% 
  group_by(Population) %>% 
  filter(Segregating.Sites >= (max(Segregating.Sites)*as.numeric(args[1]))) %>% # for terminal-based scripting
  # filter(Segregating.Sites >= (max(Segregating.Sites)*0.9)) %>% # for IDE-based scripting
  arrange(desc(Projection)) %>% 
  slice_head(n=1) %>%
  ungroup() %>% 
  droplevels() %>% 
  as.data.frame()

# Create a new data frame based on the combinations... should work for a data frame of any number of rows
combinations <- combn(seq_len(nrow(temp)), 2, simplify = FALSE)

metadata <- do.call(rbind, lapply(combinations, function(idx) {
  data.frame(
    pair = paste(sort(c(temp$Population[idx[1]], temp$Population[idx[2]])), collapse = "."),
    pop1 = temp$Population[idx[1]],
    pop2 = temp$Population[idx[2]],
    proj1 = temp$Projection[idx[1]],
    proj2 = temp$Projection[idx[2]],
    vcf = args[2]
  )
}))

metadata <- metadata[rep(1:nrow(metadata), each=args[3]),] # repeats each row of the data frame $iter number of times

write.table(metadata, "/global/scratch/users/kericlamb/Hannuus_moments3/data/moments_metadata.txt", quote = F, row.names = F, sep='\t')
