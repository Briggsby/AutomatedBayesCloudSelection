import deployers
import config_selectors as selectors
import log_converters as converters
import os
import json
import subprocess
from datetime import datetime

def standard_test(job_id, params):
	# Get base directory from file path
	base_dir = os.path.dirname(os.path.realpath(__file__))
	os.chdir(base_dir)
	# Set the folder
	os.makedirs("jobfiles/"+str(job_id), exist_ok=True)
	os.chdir(base_dir)
	# Start the config dictionary
	config = {"job_id": job_id, "params": params,
			  "timestamp": datetime.now().strftime("%Y%m%d%H%M%S"),
			  "base_dir": base_dir}

	# Instance selection
	config = getattr(selectors, config["params"]["selector"][0])(config)
	# Deployment
	config = getattr(deployers, config["params"]["deployer"][0])(config)
	# Log conversion
	config = getattr(converters, config["params"]["log_converter"][0])(config)
	# Print logs of the whole config
	config_logs = json.dumps(config)
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