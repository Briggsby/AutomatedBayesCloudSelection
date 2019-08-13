# AutomatedBayesCloudSelection
Using Bayesian Optimization and Terraform to create an automated cloud configuration selection system for any given Docker container-based application.

Prerequisites:
* Terraform v11 (Docker provider was not yet updated for v12) - https://www.terraform.io/
* jq - https://stedolan.github.io/jq/ (for merging json logs)
* Python 3.7 - https://www.python.org/download/releases/3.7/
* spearmint3 - https://github.com/briggsby/spearmint3
	* A port of spearmint from https://github.com/JasperSnoek/spearmint made to work with python3 for debugging purposes

Change the spearmint.sh file to direct to your spearmint folder (it defaults to your active site-packages folder/spearmint for python 3.7)

Instance details taken from https://www.ec2instances.info/ on 20190622 (22 June 2019)

Uses vBench benchmark from http://arcade.cs.columbia.edu/vbench/ and cloudsuite3's media streaming benchmark tool (https://github.com/parsa-epfl/cloudsuite)

Instructions (Formats for files mentioned should hopefully be intuitive from looking over them):
* In tfvars.tfvars, changing variables for your project id or credentials file locations
* In config.vars, change variables to specify what components to use or other parameters. Components (Selector, Deployer, Log_converter should be the name of the python function to be used for that component, see their corresponding python scripts for possible variables used by each component)
* In config.pb, set the variables to be searched through by spearmint. Variables should refer to column names in your 'instance_details/sampleset.csv'
* Finally, edit 'runexps.sh' according to the experiments you wish to run and stopping conditions you want spearmint to use (see spearmint repository for more details on these arguments, we have added 'eistop' and 'jobstop' which refer to the expected improvement to stop under and minimum number of samples to stop after resepectively). And run it
	* This will save experiment results, along with its job files, in 'logs/spearmint_exps/#' where # is a new folder, its name the number of experiments previously in the spearmint_exps folder.


