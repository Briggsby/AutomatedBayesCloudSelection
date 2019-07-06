import os
import numpy as np
import pandas as pd

def exact_match(config):
	# This script should take the parameters and work out
	# the instance_type to be tested

	# Import the dataset
	file_dir = os.path.dirname(os.path.realpath(__file__))
	df = pd.read_csv(file_dir +
					 "/instance_details/testset.csv", sep=",", header='infer')

	# Convert any string parameters to float that should be numeric
	config["params"]["Memory"][0] = float(config["params"]["Memory"][0])

	# Narrow down the database according to parameters
	working_df = df
	for i in config["params"]:
		if i in working_df:
			working_df = working_df[working_df[i]==config["params"][i][0]]
	

	# Return the cheapest remaining configuration
	if working_df.empty:
		config["selection"] = {"instance": None,
							   "price": None
							   }
		return config
	else:
		working_df = working_df.sort_values(by="Linux On Demand cost")
		config["selection"] = {"instance": working_df.iloc[0]["API Name"],
							   "price": working_df.iloc[0]["Linux On Demand cost"]
							   }
		return config