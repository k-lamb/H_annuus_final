# data management
library(dplyr)
library(stringr)
library(purrr)

# plotting
library(ggplot2)
library(ggpubr)
library(scales)

library(reticulate) # to run python in-line (needed for defining bounds)

setwd("~/Documents/Work MacBook/Research/paper_code/H_annuus_demography/data/moments_outputs/")

# collating data
# wd <- "1000max_everything_wildquarter_selfingall_nohyper/1000max_everything_wildquarter_selfingall_nohyper_subset" # appending directory with files... need this so we can save plots at cd ..
# wd <- "1000max_everything_wildfull_optparams_TfinancFIXED/500max_everything_wildfull_hyper_fixed_recheck"
wd <- "1000max_everything_wildfull_mininumbounds_Tfinanc/exp_fix_real/"
# wd <- "1000max_everything_wildful_boundsoptim_NwildfinalFIX_self_selfoutcross"
# wd <- "1000max_fullrun_wildfull_boundsoptim_self_selfoutcross/"
# wd <- "1000max_everything_wildfull_optparams_TfinancFIXED/1000max_subset_wildfull_hyper_optparams_wildTconT0NconADJ/updated"
self_filter = T # retain only self-self models
bucket_size <- 2 # AIC bucket size
bucket_multiplier <- 150 # multiplies bucket size for better plotting of AIC bins (bin size = bucket_size*bucket_multiplier)

lims <- "options_bounds_config_ext.py"
source_python(sprintf("%s/%s", wd, lims)) # sourcing upper/lower limits python file

# import all files into a list of data frames and combine files by matching common columns
file_list <- list.files(wd, pattern = "\\.txt$", full.names = TRUE)
data_list <- lapply(file_list, read.csv, sep="\t") 
data_list <- lapply(data_list, function(df) { df %>% mutate(T0_anc = as.numeric(T0_anc), N0_anc = as.numeric(N0_anc)) })
dat <- bind_rows(data_list, .id = "source") # add a "source" column to track the original file

# fix model column so it is more specific about the model
mod_list <- sapply(strsplit(file_list, "TV.Wild_"), function(x) x[2]) # splits off wd and pair name
mod_list <- sapply(strsplit(mod_list, ".txt"), function(x) x[1]) # splits off trailing file info

if ("mig_epoch" %in% names(dat)==F) { dat$mig_epoch <- 1 } # check if mig_epoch doesn't exist (older runs) and corrects with (accurate) dummy variable

dat$model_full <- paste0(dat$model, "_", dat$complexity, "_", dat$ancient_exp, 
                         "_", dat$shelf, "_", dat$TV_exp, "_", dat$selfing, "_", dat$selfing_all, "_", dat$mig_epoch)

dat$model.score <- ((max(dat$AIC) - min(dat$AIC))-(dat$AIC - min(dat$AIC)))/(max(dat$AIC) - min(dat$AIC))
dat <- dat %>% filter(is.na(AIC) == F) # remove weird exceptions where model iteration row is

# # weird issue where bounds suddenly not respected? might have caused an issue with running too many things at once... fixing here
# if (str_detect(wd, "divergefixed") == T) {
#   dat <- dat %>% filter(Tfinal_anc <= 5301 & Tfinal_anc >= 5299)
# }

dat_aic <- dat %>% 
  # filter(AIC <= min(AIC)*10) %>% # get rid of truly terrible models
  group_by(model_full) %>% 
  filter(is.na(AIC) == F) %>% 
  reframe(AIC.mu = mean(AIC, na.rm=T),
          AIC.median = median(AIC, na.rm=T),
          AIC.min = min(AIC, na.rm=T),
          AIC.mode = DescTools::Mode(round(as.integer(AIC)/bucket_size)*bucket_size, na.rm=T)) %>% 
  ungroup() %>% 
  group_by(model_full) %>% 
  arrange(AIC.mode) %>% 
  slice_head(n=1)

if (self_filter == T) {
  dat <- dat %>% filter(str_detect(model_full, "self_self") == T)
  dat_aic <- dat_aic %>% filter(str_detect(model_full, "self_self") == T)
}

dat_aic2 <- dat %>% # sometimes errors out due to other packages incidentally loaded in other scripts (related to n()). if this happens, restart R
  # filter(AIC <= min(AIC)*10) %>% # get rid of truly terrible models
  group_by(model_full) %>%
  mutate(AIC.bucket = round(AIC/bucket_size)*bucket_size) %>%
  ungroup() %>%
  group_by(model_full, AIC.bucket) %>%
  reframe(count=n()) %>%
  ungroup %>%
  group_by(model_full) %>%
  mutate(tot.count = sum(count)) %>%
  mutate(prop = count/tot.count) %>%
  arrange(desc(prop)) %>%
  slice_head(n=1)

dat_aic <- merge(dat_aic, dat_aic2, by=c("model_full"))
View(dat_aic)




# fixing labels
{exp_labels <- c(TV_noexp = "No TV expansion", TV_exp = "TV expansion")
model_labels <- c(bi_mig = "Bi-directional migration", uni_mig = "Uni-directional migration", no_mig = "No migration")
dat$shelf.fac <- factor(dat$shelf, levels=c("shelf", "noshelf"), labels=c("Shelf", "No Shelf"))
dat$model.fac <- factor(dat$model, levels=c("bi_mig", "uni_mig", "no_mig"))
dat$simple.complex <- factor(dat$complexity, levels=c("base", "hyper"), labels=c("Simple", "Complex"))
dat$ancient.expansion <- factor(dat$ancient_exp, levels=c("anc_exp", "anc_noexp"), labels=c("Expansion", "No expansion"))
dat$self.fac <- factor(dat$selfing, levels=c("self", "outcross"), labels=c("Selfing", "Outcrossing"))
dat$self_all.fac <- factor(dat$selfing_all, levels=c("self", "outcross"), labels=c("Selfing", "Outcrossing"))
dat$mig_epoch.fac <- factor(dat$mig_epoch, levels=c("1", "2"), labels=c("1", "2"))}

# Check if the ./parameter directory exists, and if not, create it
dir_path <- sprintf("%s/parameters", wd)

if (!dir.exists(dir_path)) {
  dir.create(dir_path, recursive = TRUE)  # Create the directory if it doesn't exist
  message("Directory created: ", dir_path)
} else {
  message("Directory already exists: ", dir_path)
}

# plot AIC to evaluate best models
jpeg(sprintf("%s/parameters/AIC_models_self.jpeg", wd), res=1e3, units="in", width=20, height=10)
ggplot(data=dat %>% arrange(AIC), aes(x=AIC))+
  facet_grid(TV_exp ~ model.fac * simple.complex * self_all.fac, labeller=labeller(TV_exp=exp_labels, model.fac=model_labels))+
  geom_density(aes(color=shelf.fac, linetype=ancient.expansion), alpha=0.5, fill=NA)+ # no simple vs complex model
  scale_color_manual(values=c("black", "gray50"))+
  xlab("AIC")+
  ylab("Density")+
  # xlim(c(NA, 4e4))+
  # scale_x_continuous(labels = scales::scientific)+
  theme_bw()+
  theme(axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=0.5),
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        plot.background = element_rect(fill="white"), axis.line = element_line(colour = "black"),
        legend.position = "right")+
  labs(color = "Shelf Inclusion", linetype = "Ancient Expansion")
dev.off()

# alternate presentation of AIC data
dat2 <- dat %>% 
  filter(AIC <= (min(dat$AIC, na.rm=T)*3)) %>%
  mutate(AIC.bucket = round(AIC/(bucket_size*bucket_multiplier))*(bucket_size*bucket_multiplier)) %>% 
  ungroup() %>% 
  group_by(AIC.bucket) %>% 
  reframe(bucket.count = n(), model_full=model_full, model=model, complexity=complexity, mig_epoch=mig_epoch,
          ancient_exp=ancient.expansion, shelf=shelf, TV_exp=TV_exp, selfing=selfing, selfing_all=selfing_all,
          model.fac=model.fac, simple.complex=simple.complex, ancient.expansion=ancient.expansion,
          self_all.fac=self_all.fac, shelf.fac=shelf.fac)

dat3 <- dat2 %>%
  group_by(model_full, AIC.bucket, bucket.count) %>% 
  reframe(mod.bucket.count = n(), model_full=model_full, model=model, complexity=complexity, mig_epoch=mig_epoch,
          ancient_exp=ancient_exp, shelf=shelf, TV_exp=TV_exp, selfing=selfing, selfing_all=selfing_all,
          model.fac=model.fac, simple.complex=simple.complex, ancient.expansion=ancient.expansion,
          self_all.fac=self_all.fac, shelf.fac=shelf.fac) %>% 
  ungroup() %>% 
  group_by(mod.bucket.count, AIC.bucket, model_full, bucket.count) %>% 
  slice_head(n=1)


# alternative AIC plotting
{
  xlimit <- 2e4 # AIC limit for bi_mig models
  a.ratio <- 1.5 # changing this will affect model1_AIC and model2_AIC differently than the other plots
  
  dat3 <- dat3 %>% 
    mutate(model_realname = case_when(
      model.fac == "bi_mig" ~ "Bi-directional migration",
      model.fac == "uni_mig" ~ "Uni-directional migration",
      model.fac == "no_mig" ~ "No migration")) %>% 
    mutate(TVexp.fac = case_when(
      TV_exp == "TV_exp" ~ "Expansion",
      TV_exp == "TV_noexp" ~ "No expansion"))
  
  dat3$model_realname <- factor(dat3$model_realname, levels=c("Bi-directional migration", "Uni-directional migration", "No migration"))
  
  model1_AIC <-
    ggplot(dat=dat3 %>% filter(model == "bi_mig"), aes(x=AIC.bucket, y=mod.bucket.count))+
    geom_bar(position="fill", stat="identity", aes(fill=simple.complex))+
    facet_wrap(~model.fac, labeller=labeller(model.fac=model_labels))+
    theme_bw()+
    xlim(c(NA, xlimit))+
    ylab("Proportion")+
    xlab("AIC")+
    theme(axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=0.5),
          panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
          plot.background = element_rect(fill="white"), axis.line = element_line(colour = "black"),
          legend.position = "right", aspect.ratio = a.ratio+0.12)+
    labs(fill = "Wild Complexity")
  
  model2_AIC <-
    ggplot(dat=dat3, aes(x=AIC.bucket, y=mod.bucket.count))+
    geom_bar(position="fill", stat="identity", aes(fill=model_realname))+
    # facet_wrap(~simple.complex)+
    theme_bw()+
    ylab("Proportion")+
    xlab("AIC")+
    theme(axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=0.5),
          panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
          plot.background = element_rect(fill="white"), axis.line = element_line(colour = "black"),
          legend.position = "right", aspect.ratio = a.ratio)+
    labs(fill = "Model")
  
  shelf_AIC <-
    ggplot(dat=dat3 %>% filter(model_realname == "Bi-directional migration"), aes(x=AIC.bucket, y=mod.bucket.count))+
    geom_bar(position="fill", stat="identity", aes(fill=shelf.fac))+
    # facet_wrap(~simple.complex)+
    theme_bw()+
    xlim(c(NA, xlimit))+
    ylab("Proportion")+
    xlab("AIC")+
    theme(axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=0.5),
          panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
          plot.background = element_rect(fill="white"), axis.line = element_line(colour = "black"),
          legend.position = "right", aspect.ratio = a.ratio)+
    labs(fill = "Ancient TV Shelf")
  
  TV_exp_AIC <-
    ggplot(dat=dat3 %>% filter(model_realname == "Bi-directional migration"), aes(x=AIC.bucket, y=mod.bucket.count))+
    geom_bar(position="fill", stat="identity", aes(fill=TVexp.fac))+
    facet_wrap(~simple.complex)+
    theme_bw()+
    xlim(c(NA, xlimit))+
    ylab("Proportion")+
    xlab("AIC")+
    theme(axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=0.5),
          panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
          plot.background = element_rect(fill="white"), axis.line = element_line(colour = "black"),
          legend.position = "right", aspect.ratio = a.ratio)+
    labs(fill = "TV Expansion")
  
  Anc_exp_AIC <-
    ggplot(dat=dat3 %>% filter(model_realname == "Bi-directional migration"), aes(x=AIC.bucket, y=mod.bucket.count))+
    geom_bar(position="fill", stat="identity", aes(fill=ancient_exp))+
    facet_wrap(~simple.complex)+
    theme_bw()+
    ylab("Proportion")+
    xlab("AIC")+
    xlim(c(NA, xlimit))+
    theme(axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=0.5),
          panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
          plot.background = element_rect(fill="white"), axis.line = element_line(colour = "black"),
          legend.position = "right", aspect.ratio = a.ratio)+
    labs(fill = "Ancient Expansion")
  
  selfing_AIC <-
    ggplot(dat=dat3 %>% filter(model_realname == "Bi-directional migration"), aes(x=AIC.bucket, y=mod.bucket.count))+
    geom_bar(position="fill", stat="identity", aes(fill=selfing))+
    facet_wrap(~simple.complex)+
    theme_bw()+
    ylab("Proportion")+
    xlab("AIC")+
    xlim(c(NA, xlimit))+
    theme(axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=0.5),
          panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
          plot.background = element_rect(fill="white"), axis.line = element_line(colour = "black"),
          legend.position = "right", aspect.ratio = a.ratio)+
    labs(fill = "Selfing")
  
  selfing_all_AIC <-
    ggplot(dat=dat3 %>% filter(model_realname == "Bi-directional migration"), aes(x=AIC.bucket, y=mod.bucket.count))+
    geom_bar(position="fill", stat="identity", aes(fill=self_all.fac))+
    facet_wrap(~simple.complex)+
    theme_bw()+
    ylab("Proportion")+
    xlab("AIC")+
    xlim(c(NA, xlimit))+
    theme(axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=0.5),
          panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
          plot.background = element_rect(fill="white"), axis.line = element_line(colour = "black"),
          legend.position = "right", aspect.ratio = a.ratio)+
    labs(fill = "Selfing (Wild & Anc)")
  
  mig_epoch_AIC <-
    ggplot(dat=dat3 %>% filter(model_realname == "Bi-directional migration"), aes(x=AIC.bucket, y=mod.bucket.count))+
    geom_bar(position="fill", stat="identity", aes(fill=as.factor(mig_epoch)))+
    facet_wrap(~simple.complex)+
    theme_bw()+
    ylab("Proportion")+
    xlab("AIC")+
    xlim(c(NA, xlimit))+
    theme(axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=0.5),
          panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
          plot.background = element_rect(fill="white"), axis.line = element_line(colour = "black"),
          legend.position = "right", aspect.ratio = a.ratio)+
    labs(fill = "Migration Epochs")
  
  
  pl.1 <- ggarrange(model2_AIC, model1_AIC, ncol=2, nrow=1)
  pl.2 <- ggarrange(Anc_exp_AIC, shelf_AIC, TV_exp_AIC, selfing_all_AIC, ncol=2, nrow=2)
  pl.final <- ggarrange(pl.1, pl.2, ncol=2)
  
  if ((length(unique(dat3$simple.complex)) == 1) & (length(unique(dat3$selfing)) == 1)){
    pl.2 <- ggarrange(Anc_exp_AIC, shelf_AIC, TV_exp_AIC, ncol=2, nrow=2)
    pl.final <- ggarrange(model2_AIC, pl.2, ncol=2, nrow=1)
  }
  
  # for models with selfing & outcrossing TV and/or multiple migration episodes:
  if ((length(unique(dat3$selfing)) > 1) == T) {
    pl.final <- ggarrange(pl.2, Anc_exp_AIC, shelf_AIC, TV_exp_AIC, selfing_AIC, selfing_all_AIC, ncol=4, nrow=2)
  }
  if ((length(unique(dat3$mig_epoch)) > 1) == T) {
    pl.final <- ggarrange(pl.2, Anc_exp_AIC, shelf_AIC, TV_exp_AIC, selfing_all_AIC, mig_epoch_AIC, ncol=4, nrow=2)
  }
  if (((length(unique(dat3$mig_epoch)) > 1) == T) & ((length(unique(dat3$selfing)) > 1) == T)) {
    pl.final <- ggarrange(pl.2, Anc_exp_AIC, shelf_AIC, TV_exp_AIC, selfing_AIC, selfing_all_AIC, mig_epoch_AIC, ncol=4, nrow=2,
                          common.legend = T)
  }
  
  jpeg(sprintf("%s/parameters/AIC_buckets.jpeg", wd), res=1e3, units="in", width=30, height=10)
  print(pl.final)
  dev.off()
}



dat_base <- dat3 %>% filter(complexity=="base")
dat_hyper <- dat3 %>% filter(complexity=="hyper")

dat_base$model_sub <- sapply(str_split(dat_base$model_full, "base_"), function(x) x[2])
dat_hyper$model_sub <- sapply(str_split(dat_hyper$model_full, "hyper_"), function(x) x[2])

if ((dim(dat_base)[1] > 0) == T) {
  jpeg(sprintf("%s/parameters/AIC_base_buckets.jpeg", wd), res=1e3, units="in", width=15, height=10)
  print(
    ggplot(dat=dat_base, aes(x=AIC.bucket, y=mod.bucket.count))+
      geom_bar(position="fill", stat="identity", aes(fill=model_sub))+
      theme_bw()+
      facet_wrap(~model, scales = "free_x")+
      theme(axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=0.5),
            panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
            plot.background = element_rect(fill="white"), axis.line = element_line(colour = "black"),
            legend.position = "right")
  )
  dev.off()
}

if ((dim(dat_hyper)[1] > 0) == T) {
  jpeg(sprintf("%s/parameters/AIC_hyper_buckets.jpeg", wd), res=1e3, units="in", width=15, height=10)
  print(
    ggplot(dat=dat_hyper, aes(x=AIC.bucket, y=mod.bucket.count))+
      geom_bar(position="fill", stat="identity", aes(fill=model_sub))+
      theme_bw()+
      facet_wrap(~model, scales = "free_x")+
      theme(axis.text.x = element_text(angle = 45, vjust = 0.5, hjust=0.5),
            panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
            plot.background = element_rect(fill="white"), axis.line = element_line(colour = "black"),
            legend.position = "right")
    )
  dev.off()
}

# plot parameters with best model indicator
best <- TRUE # plot best model (in solid blue)
converged <- TRUE # plot converged model (in dotted orchid)
mu <- FALSE # plot median model (in dashed red)
bounds <- FALSE # whether to include bounds as dashed gray lines

for (i in 1:length(unique(dat$model_full))){
  frac.mod <- 1
  ord.mag <- 1
  
  plot_list <- list()
  print(paste0("plotting: ", unique(dat$model_full)[i]))
  
  # remove columns that are all NA's for a given model (meaning model did not have these)
  dat_temp <- dat %>% 
    filter(model_full == unique(dat$model_full)[i]) %>% 
    # filter(AIC <= (min(AIC, na.rm=T))*10) %>% 
    dplyr::select(where(~ !all(is.na(.)))) %>%
    dplyr::select(where(is.numeric)) %>% 
    droplevels()
  
  # make list of variables to create plots for
  col_list <- str_detect(names(dat_temp), str_c(c("TV", "Wild", "_anc", "rate"), collapse = "|"))
  col_list <- names(dat_temp)[col_list]
  
  # ggplot annotations for ∆AIC
  AIC.min <- dat_temp %>% arrange(AIC) %>% slice_head(n=1) %>% dplyr::select(AIC) %>% as.numeric()
  
  AIC.mode <- dat_temp %>% 
    mutate(AIC.bucket = round(AIC/2)*2) %>% 
    group_by(AIC.bucket) %>% 
    reframe(count = n()) %>% 
    filter(count == max(count)) %>% 
    dplyr::select(AIC.bucket)
  AIC.mode <- AIC.mode$AIC.bucket
  AIC.delta <- AIC.mode-AIC.min
  
  for (x in 1:length(col_list)){
    dat_stat <- dat_temp %>%
      arrange(AIC) %>%
      slice_head(n=as.integer(dim(.)[1]*frac.mod)) %>% # takes top frac.mod% of models to find appropriate xlim
      reframe(mean = mean(!!sym(col_list[x]), na.rm=T), sd = sd(!!sym(col_list[x]), na.rm=T),
              sample.n = as.integer(dim(dat_temp)[1]*frac.mod))
    
    most_common <- dat_temp %>% 
      mutate(AIC.bucket = round(AIC/bucket_size)*bucket_size) %>% 
      filter(AIC.bucket == DescTools::Mode(AIC.bucket)) %>% 
      reframe(variable = mean(!!sym(col_list[x]), na.rm=T)) %>% 
      as.numeric()
    
    best_mod <- dat_temp %>% 
      filter(AIC == min(AIC)) %>% 
      reframe(variable = mean(!!sym(col_list[x]), na.rm=T)) %>% 
      as.numeric()
    
    mu_mod <- dat_temp %>% 
      reframe(variable = median(!!sym(col_list[x]), na.rm=T)) %>% 
      as.numeric()
    
    annotations <- data.frame(xpos=c(-Inf), ypos=c(Inf), hjustvar=c(-0.1), vjustvar=c(1.25), annotateText = sprintf("parameter: %.2e", most_common))
    annotations_best <- data.frame(xpos=c(-Inf), ypos=c(Inf), hjustvar=c(-0.1), vjustvar=c(2.5), annotateText = sprintf("parameter: %.2e", best_mod))
    annotations_mu <- data.frame(xpos=c(-Inf), ypos=c(Inf), hjustvar=c(-0.1), vjustvar=c(3.75), annotateText = sprintf("parameter: %.2e", mu_mod))
    
    p <- ggplot()+
      geom_density(data = dat_temp, aes(x = !!sym(col_list[x])))+
      theme_bw()+ 
      theme(axis.text.x = element_text(angle = 45, vjust = 0.5, hjust = 0.5),
            panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
            plot.background = element_rect(fill = "white"), axis.line = element_line(colour = "black"),
            legend.position = "none")+
      ylab("")
      
    # add limits for all variables but migration (squishes it and makes it impossible to see)
    if (str_detect(col_list[x], "Mig") == FALSE) {
      if (str_detect(col_list[x], "Tfinal_anc") == FALSE) {
        if (bounds == TRUE) {
          p <- p +
            xlim(as.numeric(get(sprintf("%s_lower", col_list[x]))), as.numeric(get(sprintf("%s_upper", col_list[x]))))+ 
            geom_vline(xintercept=as.numeric(get(sprintf("%s_lower", col_list[x]))), linetype=2, linewidth=0.5, color="gray50")+
            geom_vline(xintercept=as.numeric(get(sprintf("%s_upper", col_list[x]))), linetype=2, linewidth=0.5, color="gray50")
        }
        
        else {
          grand <- max((dat_temp %>% filter(AIC == min(AIC)) %>% dplyr::select(col_list[x])) %>% slice_head(n=1) %>% as.numeric(), # best by AIC
                       most_common) # converged model
          div.mult <- 3
          p <- p + xlim(c((most_common*(1/div.mult)), (most_common*div.mult)))
        } 
      }
    }
    
    # add converged model solution
    if (converged == T) {
      p <- p + 
        geom_vline(xintercept=most_common, linetype=3, linewidth=2, color="orchid3", alpha=1)+ # converged model solution
        geom_text(data=annotations,aes(x=xpos,y=ypos,hjust=hjustvar,vjust=vjustvar,label=annotateText), color="orchid3")
    }
    
    if (best == T) {
      p <- p +
        geom_vline(xintercept=((dat_temp %>% filter(AIC == min(AIC)) %>% dplyr::select(col_list[x])) %>% slice_head(n=1) %>% as.numeric()),
                   linetype=1, linewidth=1, color="blue", alpha=1)+ # best model
        geom_text(data=annotations_best,aes(x=xpos,y=ypos,hjust=hjustvar,vjust=vjustvar,label=annotateText), color="blue")
    }
    
    if (mu == T) {
      p <- p +
        geom_vline(xintercept=mu_mod, linetype=2, linewidth=1, color="red3", alpha=1)+ # mean model solution
        geom_text(data=annotations_mu,aes(x=xpos,y=ypos,hjust=hjustvar,vjust=vjustvar,label=annotateText), color="red3")
    }

    plot_list <- append(plot_list, list(p)) # append plot into growing list for the given model
  }
  
  # save plot arrangement details & aggregated plot
  nrow <- 4
  ncol <- length(plot_list)/nrow
  g <- ggarrange(plotlist = plot_list, ncol = as.integer(ncol+1), nrow = nrow)
  
  jpeg(sprintf("%s/parameters/%s_parameters.jpeg", wd, unique(dat$model_full)[i]), units="in", res=1e3, width=30, height=15)
  print(g) # doesn't work if you don't print it. don't know why.
  dev.off()
}



# plot it like Peter's graphs
n=10 # number of points in spline fitting

# For best model:
model <- dat %>% 
  filter(model_full == (dat_aic %>% arrange(AIC.min) %>% slice_head(n=1))$model_full) %>% 
  filter(AIC == min(AIC))
mod_n <- model$model_full

# For most converged model:
model <- dat %>% 
  filter(model_full == (dat_aic %>% arrange(AIC.mode) %>% slice_head(n=1))$model_full & AIC <= min(dat_aic$AIC.mode)+2 & AIC >= min(dat_aic$AIC.mode)-2) %>% 
  slice_head(n=1)
mod_n <- model$model_full

# data prep. runs as a block.
{
  # Ancestral
  {
    if (str_detect(mod_n, "anc_exp") == T) {
      anc.dat <- data.frame(pop = rep("Anc", 3), time=c(model$T0_anc, model$T1_anc, model$Tfinal_anc), 
                            size=c(model$N0_anc, model$N1_anc, model$Nfinal_anc))
    }
    else {
      anc.dat <- data.frame(pop = rep("Anc", 2), time=c(model$T0_anc, model$Tfinal_anc), size=c(model$N0_anc, model$Nfinal_anc))
    }
  }
  
  # TV
  {
    if (str_detect(mod_n, "noshelf") == T & str_detect(mod_n, "TV_noexp") == T) {
      tv.dat <- data.frame(pop = rep("TV", 2), time=c(model$Tfinal_anc, 0), size=c(model$N0_TV, model$Ncon_TV))
    }
    
    if (str_detect(mod_n, "_shelf") == T & str_detect(mod_n, "TV_noexp") == T) {
      tv.dat <- data.frame(pop = rep("TV", 3), time=c(model$Tfinal_anc, model$Tshelf_TV, 0), 
                           size=c(model$N0_TV, model$Nshelf_TV, model$Ncon_TV))
    }
    if (str_detect(mod_n, "noshelf") == T & str_detect(mod_n, "TV_exp") == T) {
      tv.dat <- data.frame(pop = rep("TV", 3), time=c(model$Tfinal_anc, model$Tcon_exp_TV, 0), 
                           size=c(model$N0_TV, model$Ncon_TV, model$Nexp_TV))
    }
    
    if (str_detect(mod_n, "shelf") == T & str_detect(mod_n, "TV_exp") == T) {
      tv.dat <- data.frame(pop = rep("TV", 4), time=c(model$Tfinal_anc, model$Tshelf_TV, model$Texp_TV, 0), 
                           size=c(model$N0_TV, model$Nshelf_TV, model$Ncon_TV, model$Nexp_TV))
    }
  }
  
  # Wild 
  {
    if (str_detect(mod_n, "hyper") == T) {
      wild.dat <- data.frame(pop = rep("Wild", 4), time=c(model$Tfinal_anc, model$T0_Wild, model$Tcon_Wild, 0), 
                             size=c(model$N0_Wild, model$N0exp_Wild, model$Ncon_Wild, model$Nfinal_Wild))
    }
  }
  
  mod.dat <- rbind(anc.dat, tv.dat, wild.dat)
  
  
  # trying alternative to spline fitting the points (make the connections straighter)
  # ancestral
  grid <- data.frame(time = numeric(), size = numeric())
  for (i in 1:(nrow(anc.dat) - 1)) {
    temp <- data.frame(time=seq(anc.dat$time[i], anc.dat$time[(i+1)], length.out=n),
                       size=seq(anc.dat$size[i], anc.dat$size[(i+1)], length.out=n))
    grid <- rbind(grid, temp)
  }
  anc.dat.straight <- data.frame(pop=rep("Anc", dim(grid)[1]), time=grid$time, size=grid$size)
  
  # TV
  grid <- data.frame(time = numeric(), size = numeric())
  for (i in 1:(nrow(tv.dat) - 1)) {
    temp <- data.frame(time=seq(tv.dat$time[i], tv.dat$time[(i+1)], length.out=n),
                       size=seq(tv.dat$size[i], tv.dat$size[(i+1)], length.out=n))
    grid <- rbind(grid, temp)
  }
  TV.dat.straight <- data.frame(pop=rep("TV", dim(grid)[1]), time=grid$time, size=grid$size)
  
  # Wild
  grid <- data.frame(time = numeric(), size = numeric())
  for (i in 1:(nrow(wild.dat) - 1)) {
    temp <- data.frame(time=seq(wild.dat$time[i], wild.dat$time[(i+1)], length.out=n),
                       size=seq(wild.dat$size[i], wild.dat$size[(i+1)], length.out=n))
    grid <- rbind(grid, temp)
  }
  Wild.dat.straight <- data.frame(pop=rep("Wild", dim(grid)[1]), time=grid$time, size=grid$size)
  
  
  # Geom_smooth fitting is rough... adding spline fit points for smoother plotting
  # ancestral
  spline_points <- data.frame(time = numeric(), size = numeric())
  for (i in 1:(nrow(anc.dat) - 1)) {
    spline_result <- as.data.frame(spline(anc.dat$time[i:(i+1)], anc.dat$size[i:(i+1)], n = n)) # 50 intermediate points
    spline_points <- rbind(spline_points, spline_result %>% map_df(rev))
  }
  anc.dat.spline <- data.frame(pop=rep("Anc", dim(spline_points)[1]), time=spline_points$x, size=spline_points$y)

  # TV
  spline_points <- data.frame(time = numeric(), size = numeric())
  for (i in 1:(nrow(tv.dat) - 1)) {
    spline_result <- as.data.frame(spline(tv.dat$time[i:(i+1)], tv.dat$size[i:(i+1)], n = n)) # 50 intermediate points
    spline_points <- rbind(spline_points, spline_result %>% map_df(rev))
  }
  tv.dat.spline <- data.frame(pop=rep("TV", dim(spline_points)[1]), time=spline_points$x, size=spline_points$y)

  # Wild
  spline_points <- data.frame(time = numeric(), size = numeric())
  for (i in 1:(nrow(wild.dat) - 1)) {
    spline_result <- as.data.frame(spline(wild.dat$time[i:(i+1)], wild.dat$size[i:(i+1)], n = n)) # 50 intermediate points
    spline_points <- rbind(spline_points, spline_result %>% map_df(rev))
  }
  wild.dat.spline <- data.frame(pop=rep("Wild", dim(spline_points)[1]), time=spline_points$x, size=spline_points$y)

  # final compilation
  mod.dat.spline <- rbind(anc.dat.spline, tv.dat.spline, wild.dat.spline)
  mod.dat.straight <- rbind(anc.dat.straight, TV.dat.straight, Wild.dat.straight)
  
}

# Peter data approximation
smc <- data.frame(pop=c(rep("Anc", 3), rep("TV", 4), rep("Wild", 4)), 
                  time=c(c(100000, 7582, 5359), c(5359, 1349, 361, 0), c(5359, 3190, 492, 0)), 
                  size=c(c(100000, 8275, 12181), c(12181, 1768, 59628, 40000), c(12181, 26451, 10207, 20000)))

# plotting
ggplot(data=mod.dat, aes(x=time+1, y=size, color=pop))+
  # scale_y_continuous(limit=c(0,(max(mod.dat$size)*1.2)))+
  # geom_smooth(method="glm", formula=y ~ poly(x, 4), linewidth=1, alpha=0.5, se=F)+
  geom_line(linewidth=1, alpha=0.5)+
  geom_line(data=smc, aes(x=time+1, y=size, color=pop), linewidth=0.5, alpha=0.5, linetype=2)+
  geom_point(data=smc, aes(x=time+1, y=size, color=pop), alpha=0.5, shape=0)+
  geom_point(data=mod.dat, aes(x=time+1, y=size, color=pop), shape=15)+
  scale_x_log10()+
  scale_y_log10(limits=c(1e1,1e6))+
  xlab("Years Before Present")+
  ylab("Effective Population Size (Ne)")+
  annotation_logticks()+
  geom_vline(xintercept = model$Tmig_WildTV, linetype=3, color="gray50")+
  theme_bw()+
  theme(text = element_text(size=12), legend.position = "right", aspect.ratio=0.75,
        panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
        plot.background = element_rect(fill="white"), axis.line = element_line(colour = "black"))

# to get deme plots in terminal below, run this:
# cd ~/Documents/Research/paper_code/H_annuus_demography/Hannuus_moments_og
# python ./code/moments_scripts/converge_plot.py ${model_run_folder} ${con/best}
# converge_plot is in H_annuus...og3, con = converged, best = best by AIC
