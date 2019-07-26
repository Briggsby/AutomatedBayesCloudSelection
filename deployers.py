from python_terraform import Terraform
import os
import docker
import re
import signal
import time
import json
from functools import partial
import kubernetes as kube
from random import gauss

def keyboard_interrupt_handler(instance_tf, config, signal, frame):
	print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
	vm_destroy(config, instance_tf)
	exit(0)

def simulate_vbench(config):
	score_dists = {
		"c5.2xlarge": [0.735389704489885, 0.0090144001870981],
		"c5.large": [0.685901426610771, 0.00606817170842319],
		"c5.xlarge": [0.741317303702905, 0.00914818797616337],
		"m5.2xlarge": [0.670288711168783, 0.0203019184176524],
		"m5.large": [0.609520664271226, 0.00306456396111854],
		"m5.xlarge": [0.652927691499056, 0.00625981402157845],
		"n1-highcpu-2": [0.479268071924939, 0.00837194519313252],
		"n1-highcpu-4": [0.5145565552674, 0.0107097320337508],
		"n1-highcpu-8": [0.51362270897615, 0.011674931393599],
		"n1-highmem-2": [0.486284158528833, 0.00524964091477984],
		"n1-highmem-4": [0.514716289876, 0.0111786054410824],
		"n1-highmem-8": [0.51876978323085, 0.0145250385568328],
		"n1-standard-2": [0.484797375655976, 0.00711115462005657],
		"n1-standard-4": [0.51102065121265, 0.0100261784206764],
		"n1-standard-8": [0.509472112443391, 0.0206690071921936],
		"r5.2xlarge": [0.6607181025834, 0.0118908863090462],
		"r5.large": [0.62428610571595, 0.0168857431525331],
		"r5.xlarge": [0.657909086988129, 0.00847214059316436]
	}

	score = gauss(score_dists[config['selection']['instance']][0], 
				  score_dists[config['selection']['instance']][1])

	config["logs"] = f"b,b,b,b,b,b,b,b,{score}"
	return config

def ping_testserver(config):
	config, instance_tf, ip = vm_provision(config)

	print("Deploying test server")

	client = docker.DockerClient(base_url='tcp://'+ip+':2376')
	client.images.pull("briggsby/vbench:notvbenchprimetestserver")
	client.containers.run("briggsby/vbench:notvbenchprimetestserver", ports={'80/tcp':8000}, detach=True)

	print("Setting up kubernetes pinging cluster")

	kube.config.load_kube_config(config_file=config["base_dir"]+"/instance_deploy/google/credentials/kube-test")
	client = kube.client.ApiClient()
	v1 = kube.client.CoreV1Api()
	extv1 = kube.client.ExtensionsV1beta1Api()
	cmap = kube.client.V1ConfigMap()

	cmap.metadata = kube.client.V1ObjectMeta(name="ping-config")
	cmap.data = {
		"IPTARGET" : ip,
		"PORTTARGET":"8000",
		"PINGTIME": "10",
		}

	v1.create_namespaced_config_map(namespace="default", body=cmap)
	
	kube.utils.create_from_yaml(client, config["base_dir"]+"/instance_deploy/files/exampleping.yaml")

	print("Waiting for pings")

	time.sleep(45)

	print("Collecting logs and deleting resources")

	ret = v1.list_pod_for_all_namespaces(watch=False)
	logs = {}
	for i in ret.items:
		if "curl-test" in i.metadata.name:
			pod = i.metadata.name
			logs[pod] = v1.read_namespaced_pod_log(pod, namespace="default")

	v1.delete_namespaced_config_map(namespace="default", name=cmap.metadata.name)
	extv1.delete_namespaced_daemon_set(namespace="default", name="curl-test")

	for i in ret.items:
		if "curl-test" in i.metadata.name:
			pod = i.metadata.name
			v1.delete_namespaced_pod(name=pod, namespace="default")

	time.sleep(20)

	config["logs"] = json.dumps(logs, indent=2)

	if instance_tf is not None:
		vm_destroy(config, instance_tf)
	return config


def vbench(config):
	config, instance_tf, ip = vm_provision(config)
	client = docker.DockerClient(base_url='tcp://'+ip+':2376')
	client.images.pull("briggsby/vbench:ubuntu")

	vbench_type = config["vars"]["vbench_type"]
	vbench_filter = config["vars"]["vbench_filter"]

	print("Performing vbench benchmark")
	logs = client.containers.run("briggsby/vbench:ubuntu", f"{vbench_type} {vbench_filter}")
	print(logs)
	config["logs"] = str(logs, 'utf-8')
	if instance_tf is not None:
		vm_destroy(config, instance_tf)
	return config

def cloudsuite3_media(config, ip, instance_tf=None):

	print("Preparing cloudsuite")

	client = docker.DockerClient(base_url='tcp://'+ip+':2376')
	client.containers.prune()
	client.images.pull("cloudsuite/media-streaming", "dataset",)
	client.containers.create("cloudsuite/media-streaming:dataset", name="streaming_dataset")
	client.networks.create("streaming_network")
	client.images.pull("cloudsuite/media-streaming", "server")
	client.containers.run("cloudsuite/media-streaming:server", detach=True, name="streaming_server", 
	volumes_from=["streaming_dataset"], network="streaming_network")
	# client.images.pull("cloudsuite/media-streaming", "client")
	image = client.images.build(path=config["base_dir"]+"/instance_deploy/files/cloudsuite_media_client",
	tag = "mine/media-streaming-client")

	# These are values that have been found to reduce times to acceptable levels
	# while still insuring max sessions is not too low
	max_sess_dict = {"aws" : {2:60000, 4:2000000, 8:2000000}, "google": {2:8000, 4: 100000, 8: 800000}}
	max_sessions = max_sess_dict[config["params"]["Provider"][0]][int(config["params"]["CPU"][0])]

	num_sessions = 8

	print("Running cloudsuite")

	logs = client.containers.run("mine/media-streaming-client", f"streaming_server {max_sessions} {num_sessions}",
	 tty=True, name="streaming_client", volumes={'/logs': {'bind': '/output', 'mode': 'rw'}},
	  volumes_from=["streaming_dataset"], network="streaming_network", )

	print("Cloudsuite finished")

	config["logs"] = str(logs, 'utf-8')

	if instance_tf is not None:
		vm_destroy(config, instance_tf)
	return config

def docker_deploy(config, ip, instance_tf=None):
	client = docker.DockerClient(base_url='tcp://'+ip+':2376')
	logs = client.containers.run(config["vars"]["docker_image"], **config["vars"]["docker_params"])

	config["logs"] = str(logs, 'utf-8')

	if instance_tf is not None:
		vm_destroy(config, instance_tf)
	return config

def sys_docker_deploy(config, ip, instance_tf=None):
	client = docker.DockerClient(base_url='tcp://'+ip+':2376')
	logs = client.containers.run(config["vars"]["docker_image"],
	 command='sysbench --test=cpu --cpu-max-prime=5000 run')

	config["logs"] = str(logs, 'utf-8')

	if instance_tf is not None:
		vm_destroy(config, instance_tf)
	return config

def vm_cloudsuite3_media_deploy(config):
	config, instance_tf, ip = vm_provision(config)
	config = cloudsuite3_media(config, ip, instance_tf)
	return config

def vm_docker_deploy(config):
	config, instance_tf, ip = vm_provision(config)
	config = docker_deploy(config, ip, instance_tf)
	return config

def vm_destroy(config, instance_tf):
	tfstate_path = config["base_dir"] + '/tf_states/' + str(config["job_id"])
	instance_tf.init(backend_config={'path':tfstate_path + '/terraform.tfstate'})
	instance_tf.destroy(auto_approve=True, var_file=config["base_dir"]+"/tfvars.tfvars")

def vm_provision(config):

	print(f"Provisioning {config['selection']['instance']} instance from {config['params']['Provider']}")

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
	signal.signal(signal.SIGINT, partial(keyboard_interrupt_handler, instance_tf, config))
	apply = instance_tf.apply(var_file=tfvars, lock=False,
	var={'instance_type':config["selection"]["instance"]}, skip_plan=True)
	print(apply)

	find = re.search(r"docker_host_ip = [\d.]+", apply[1])
	instance_ip = apply[1][(find.regs[0][0]+17):find.regs[0][1]]
	

	# instance_tf.init(backend_config={'path':tfstate_path + '/terraform.tfstate'})
	# instance_ip = instance_tf.output()["docker_host_ip"]["value"]
	
	print(f"{config['selection']['instance']} instance created at {instance_ip}")

	return config, instance_tf, instance_ip

def fake_deploy(config):
	# Returns logs as though it did vm_docker_deploy with sysbench

	# file_dir = os.path.dirname(os.path.realpath(__file__))
	time.sleep(10)
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
	instance_tf.apply(var_file=tfvars, lock=False,
	var={'instance_type':config["selection"]["instance"]}, skip_plan=True)

	docker_tf.init(backend_config={'path':tfstate_path + '/docker_tfstate/terraform.tfstate'})
	docker_tf.apply(var_file=tfvars, lock=False, var={'tfstate_path':tfstate_path}, skip_plan=True)

	docker_tf.init(backend_config={'path':tfstate_path + '/docker_tfstate/terraform.tfstate'})
	logs = docker_tf.output()
	config["logs"] = logs
	docker_tf.init(backend_config={'path':tfstate_path + '/docker_tfstate/terraform.tfstate'})
	docker_tf.destroy(auto_approve=True)
	instance_tf.init(backend_config={'path':tfstate_path + '/terraform.tfstate'})
	instance_tf.destroy(auto_approve=True)

	return config
