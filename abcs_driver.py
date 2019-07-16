import deployers
import config_selectors as selectors
import log_converters as converters
import os
import json
import subprocess
import numpy as np
from datetime import datetime


def standard_test(job_id, params):
	# Get base directory from file path
	base_dir = os.path.dirname(os.path.realpath(__file__))
	os.chdir(base_dir)
	# Set the folder
	os.makedirs("jobfiles", exist_ok=True)
	os.chdir(base_dir)
	# Get the variables
	fp = open(base_dir+"/config.vars", "r")
	variables = json.load(fp)
	fp.close()
	# Start the config dictionary
	config = {"job_id": job_id, "params": params, "vars": variables,
			  "timestamp": datetime.now().strftime("%Y%m%d%H%M%S"),
			  "base_dir": base_dir}

	# Instance selection
	config = getattr(selectors, config["vars"]["selector"])(config)
	# Deployment
	config = getattr(deployers, config["vars"]["deployer"])(config)
	# Log conversion
	config = getattr(converters, config["vars"]["log_converter"])(config)
	# Print logs of the whole config
	print("Total configuration test details:")
	print(config)
	config_logs = json.dumps(config, cls=NumpyEncoder)
	logfile = open("jobfiles/"+str(job_id)+".json", "w+")
	logfile.write(config_logs)
	logfile.close()
	
	# Full log merging
	logfile = open("logs/newestlogs.json", "w+")
	logfile.write(config_logs)
	logfile.close()
	subprocess.call(["./logmerger.sh"], cwd=base_dir+"/logs/")

	# Return final value
	return config["value"]


class NumpyEncoder(json.JSONEncoder):
	# An encoder for json dumping nested dictionaries with numpy array components
	# From: https://stackoverflow.com/questions/26646362/numpy-array-is-not-json-serializable
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def main(job_id, params):
	print('Anything printed here will end up in the output directory for job #:', str(job_id))
	print(params)
	return standard_test(job_id, params)
