### H_annuus_final -- demographic inference using Moments

##### How the pipeline works:
 - The script takes a VCF file pre-filtered for unlinked SNPs and checks missingness within SNPs and within individuals
    - filters the VCF in prep_pipeline.sh and exports a new VCF used here with {file_name}_filter.vcf
 - Determine optimal projection for Moments using easySFS (https://github.com/isaacovercast/easySFS). this is done by:
    - auto-create a custom environment for Moments and easySFS
    - generate a population map for Moments/easySFS using: popmap.R
    - generate easySFS files (./code/easySFS.py) and save them to: ./data/easySFS_output.txt
    - digest raw easySFS outputs into readable table using: ./code/projection_digest.py
    - generate metadata file for Moments: ./code/metadata.R
        - threshold for sites retained in easySFS projection as a proportion of the maximum. defaults to 90%. this should balance the tradeoff resolution of the SFS (i.e., the dimensions) and the depth of each pixel in the SFS (i.e., how many sites are used)
 - Running the Moments section of the pipeline:
    - several options exist for running Moments models. for debugging (debug) or (subset) runs, use those. Otherwise, use the (full_run) option
        - these options pass the desired combinations of model parameters to explore onto the for loop statements below
    - several scripts enable models to be written and passed onto the Hannuus.sh/.py scripts. These are:
        - options_bounds_config.py --> provides the bounds information for the options file. silently called in the ...options_ext.py file
        - model_scribe_options_ext.py --> this script creates the .yaml options file for models required by demes/Moments
        - model_scribe_ext.py --> two options (Template==T/F) create the .yaml model and model template files required by demes/Moments to run the models (F) or plot them (T)
    - Hannuus.sh/.py:
        - Hannuus.sh ensures the Moments custom environment exists (and if not creates it) and runs the .py scripts
        - Hannuus.py optimizes each model, running $iter_multiplier number of runs per job. This is done to cut down on total number of jobs submitted to HPC. Outputs are saved to a folder specified by the user
        - bestmodel_plot.py plots the best model by AIC, iteratively overwriting worse models
        - convergemodel_plot.py plots the most converged model solution (by AIC)
 - Analysis:
    - plotting and analysis of the models is handled by: Hannuus_autoprocess_update.R
        - this script handles aggregating model outputs and can plot outputs for both best converged model (by AIC) and best model by AIC


 
