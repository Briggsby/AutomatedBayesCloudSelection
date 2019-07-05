import numpy as np
import pandas as pd

def main(job_id, params, base_dir):
	# This script should take the parameters and work out
	# the instance_type to be tested
	
	provider = "aws"
	instance_type = None

	# Import the dataset
	df = pd.read_csv(base_dir + "/instance_details/testset.csv", sep=",", header='infer')
	working_df = df

	params["Memory"][0] = float(params["Memory"][0])

	for i in params:
		working_df = working_df[working_df[i]==params[i][0]]
	
	if working_df.empty:
		return None, None
	else:
		working_df = working_df.sort_values(by="Linux On Demand cost")
		return working_df.iloc[0]["API Name"], working_df.iloc[0]["Linux On Demand cost"]