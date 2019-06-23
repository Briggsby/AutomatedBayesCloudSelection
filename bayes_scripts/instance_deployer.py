from python_terraform import *
import os

# This script should deploy the instance and return the output/logs after the test has finished
def main(instance_type, provider, base_dir):
	### Setup terraform objects
	instance_wkdir = base_dir + "/instance_provider/" + provider
	instance_tf = Terraform(working_dir=instance_wkdir)
	docker_tf = Terraform(base_dir + "/docker_deploy")

	instance_tf.apply(var={'instance_type':instance_type}, skip_plan=True)
	docker_tf.apply(skip_plan=True)

	logs = instance_tf.output()
	docker_tf.destroy(auto_approve=True)
	instance_tf.destroy(auto_approve=True)

	return logs