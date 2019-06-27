from python_terraform import *
import os


def instance_test(job_id, params):
	# Get base directory of AutomatedBayesCloudSelection
	base_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__))))
	os.chdir(base_dir)

	# Variables that are for now not changed, but later may vary 
	# based on the Bayes parameters
	provider = "aws"

	# Set working directory to appropriate provider's folder
	instance_wkdir = base_dir + "/instance_deploy/" + provider
	os.chdir(instance_wkdir)

	# Find instance these params suggest should be tested
	instance_selector = __import__("instance_selector")
	instance_type = instance_selector.main(job_id, params)
	# Run test on that instance, get its logs
	instance_deployer = __import__("instance_deployer")
	logs = instance_deployer.main(job_id, params, instance_type, provider, base_dir)
	print(logs)

	# This saves every log, to keep all logs ever made in one json file
	# in case other logs folders are deleted
	newlogs = open(base_dir+"/logs/newestlogs.json", "w+")
	newlogs.write(logs)
	newlogs.close()
	subprocess.call([base_dir+"/logs/logmerger.sh"], cwd=base_dir+"/logs/")

	# Convert logs into quantitative value
	log_converter = __import__("log_converter")
	value = log_converter.main(job_id, params, logs)
	# Return that value
	return value


def main(job_id, params):
	print 'Anything printed here will end up in the output directory for job #:', str(job_id)
	print params
	return instance_test(job_id, params)

main(0, [])