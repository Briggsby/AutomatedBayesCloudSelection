# AutomatedBayesCloudSelection
Using Bayesian Optimization and Terraform to create an automated cloud configuration selection system for any given Docker container-based application.

Prequisites:
Terraform v11 (Docker provider not yet updated for v12) - https://www.terraform.io/
jq - https://stedolan.github.io/jq/
Python 2.7 - https://www.python.org/download/releases/2.7/
spearmint - https://github.com/JasperSnoek/spearmint
    -- After setup and installation, must go into code and change the lines at 115-118 in the 'runner.py' file to:
        dbl_vals = list(param.dbl_val)
        int_vals = list(param.int_val)
        str_vals = list(param.str_val)

        I assume that the _values property used was removed from Google Protocol Buffer

Change the spearmint.sh file to direct to your spearmint folder (it defaults to your active site-packages folder/spearmint)