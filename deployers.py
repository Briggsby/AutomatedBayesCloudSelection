from python_terraform import Terraform
import os

def vm_docker_deploy(config):
	return config

def fake_deploy(config):
	file_dir = os.path.dirname(os.path.realpath(__file__))
	# Returns logs as though it did vm_docker_deploy_old with sysbench
	if config["selection"]["instance"] is None:
		config["logs"] = None
		return config
	
	logs = open(file_dir+"/docker_deploy/example_docker_logs.json", "r").read()
	config["logs"] = logs

	return config

def vm_docker_deploy_old(config):
	# This script should deploy the instance and return the output/logs after the test has finished

	file_dir = os.path.dirname(os.path.realpath(__file__))
	provider = config["params"]["Provider"][0]
	### Check that a selection was made
	if config["selection"]["instance"] is None:
		config["logs"] = None
		return config

	### Setup terraform objects
	instance_wkdir = file_dir + "/instance_deploy/" + provider
	instance_tf = Terraform(working_dir=instance_wkdir)
	docker_tf = Terraform(file_dir + "/docker_deploy")
	
	tfstate_path = config["base_dir"] + '/tf_states/' + str(config["job_id"])
	tfvars = config["base_dir"]+"/tfvars.tfvars"

	## ALSO DIRECT TO A VARS.TF IN THE BASE_DIR
	instance_tf.init(backend_config={'path':tfstate_path + '/terraform.tfstate'})
	instance_tf.apply(var_file=tfvars,
	var={'instance_type':config["selection"]["instance"]}, skip_plan=True)

	docker_tf.init(backend_config={'path':tfstate_path + '/docker_tfstate/terraform.tfstate'})
	docker_tf.apply(var_file=tfvars, var={'tfstate_path':tfstate_path}, skip_plan=True)

	logs = docker_tf.output()
	config["logs"] = logs
	docker_tf.destroy('-lock=false', auto_approve=True)
	instance_tf.destroy('-lock=false', auto_approve=True)

	return config