from python_terraform import Terraform
import os
import docker

def docker_deploy(config, ip, instance_tf=None):
	client = docker.DockerClient(base_url='tcp://'+ip+':2376')
	logs = client.containers.run(config["params"]["docker_image"][0],
	 command='sysbench --test=cpu --cpu-max-prime=5000 run')

	config["logs"] = str(logs, 'utf-8')

	if instance_tf is not None:
		instance_tf.destroy(auto_approve=True)
	return config

def vm_docker_deploy(config):
	config, instance_tf, ip = vm_provision(config)
	config = docker_deploy(config, ip, instance_tf)
	return config

def vm_provision(config):
	file_dir = os.path.dirname(os.path.realpath(__file__))
	provider = config["params"]["Provider"][0]
	### Check that a selection was made
	if config["selection"]["instance"] is None:
		config["logs"] = None
		return config

	### Setup terraform objects
	instance_wkdir = file_dir + "/instance_deploy/" + provider
	instance_tf = Terraform(working_dir=instance_wkdir)
	
	tfstate_path = config["base_dir"] + '/tf_states/' + str(config["job_id"])
	tfvars = config["base_dir"]+"/tfvars.tfvars"

	instance_tf.init(backend_config={'path':tfstate_path + '/terraform.tfstate'})
	instance_tf.apply(var_file=tfvars,
	var={'instance_type':config["selection"]["instance"]}, skip_plan=True)

	instance_ip = instance_tf.output()["docker_host_ip"]["value"]

	return config, instance_tf, instance_ip

def fake_deploy(config):
	# Returns logs as though it did vm_docker_deploy with sysbench

	# file_dir = os.path.dirname(os.path.realpath(__file__))

	if config["selection"]["instance"] is None:
		config["logs"] = None
		return config
	
	# logs = open(file_dir+"/docker_deploy/example_docker_logs.json", "r").read()
	logs = str(b'sysbench 1.0.17 (using bundled LuaJIT 2.1.0-beta2)\n\nRunning the test with following options:\nNumber of threads: 1\nInitializing random number generator from current time\n\n\nPrime numbers limit: 5000\n\nInitializing worker threads...\n\nThreads started!\n\nCPU speed:\n    events per second:  2044.38\n\nGeneral statistics:\n    total time:                          10.0002s\n    total number of events:              20448\n\nLatency (ms):\n         min:                                    0.44\n         avg:                                    0.49\n         max:                                    3.91\n         95th percentile:                        0.54\n         sum:                                 9973.95\n\nThreads fairness:\n    events (avg/stddev):           20448.0000/0.00\n    execution time (avg/stddev):   9.9739/0.00\n\n', 'utf-8')
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
	docker_tf.destroy(auto_approve=True)
	instance_tf.destroy(auto_approve=True)

	return config