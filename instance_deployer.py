from python_terraform import *
import os

# This script should deploy the instance and return the output/logs after the test has finished
def main(job_id, params, instance_type, provider, base_dir):
	### Setup terraform objects
	instance_wkdir = base_dir + "/instance_deploy/" + provider
	instance_tf = Terraform(working_dir=instance_wkdir)
	docker_tf = Terraform(base_dir + "/docker_deploy")
	
	tfstate_path = base_dir + '/tf_states/' + str(job_id)

	instance_tf.init(backend_config={'path':tfstate_path + '/terraform.tfstate'})
	instance_tf.apply(var={'instance_type':instance_type}, skip_plan=True)

	docker_tf.init(backend_config={'path':tfstate_path + '/docker_tfstate/terraform.tfstate'})
	docker_tf.apply(var={'tfstate_path':tfstate_path}, skip_plan=True)

	logs = docker_tf.output()
	docker_tf.destroy(auto_approve=True)
	instance_tf.destroy(auto_approve=True)

	return logs