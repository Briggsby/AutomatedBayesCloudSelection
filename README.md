# AutomatedBayesCloudSelection
Using Bayesian Optimization and Terraform to create an automated cloud configuration selection system for any given Docker container-based application.

Prequisites:
Terraform v11 (Docker provider was not yet updated for v12) - https://www.terraform.io/
jq - https://stedolan.github.io/jq/ (for merging json logs)
Python 3.7 - https://www.python.org/download/releases/3.7/
spearmint3 - https://github.com/briggsby/spearmint3
	-- A port of spearmint from https://github.com/JasperSnoek/spearmint made to work with python3 for debugging purposes

Change the spearmint.sh file to direct to your spearmint folder (it defaults to your active site-packages folder/spearmint)

Instance details taken from https://www.ec2instances.info/ on 20190622 (22 June 2019)

Uses cloudsuite3's media streaming benchmark tool (https://github.com/parsa-epfl/cloudsuite)
