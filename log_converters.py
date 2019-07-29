import re
import json

def no_value(config):
	config["value"] = None
	return config

def ping_testserver(config):
	logs = config["logs"]
	logs = json.loads(logs,)
	inputs = []
	response_times = []
	for i in logs:
		results = logs[i].split("\n")
		for line in results:
			if "URL" in line and line != "DONE":
				split_line = line.split("\t")
				inputs.append(int(split_line[1].split('/')[1]))
				response_times.append(float(split_line[3]))
	value = -(sum(response_times)/len(response_times))
	config["value"] =  value/config["selection"]["price"]
	print("Value:", value, "Price:", config["selection"]["price"])
	return config
		

def vbench(config):
	logs = config["logs"]
	value = float(logs.split(",")[8])
	print("Value:", value, "Price:", config["selection"]["price"])
	config["value"] = -value/config["selection"]["price"]
	return config

def cloudsuite_media_stream(config):
	logs = config["logs"]

	max_sess_dict = {"aws" : {2:60000, 4:2000000, 8:2000000}, "google": {2:8000, 4: 100000, 8: 800000}}
	max_sessions = max_sess_dict[config["params"]["Provider"][0]][int(config["params"]["CPU"][0])]
	json.load

	if logs is None:
		config["value"] = None
		return config

	if type(logs) is dict:
		logs = json.dumps(log)
	
	find = re.search(r"Benchmark succeeded for maximum sessions\: [\d]+", logs)
	if find == None:
		find2 = re.search(r"Maximum limit for number of sessions too low", logs)
		if find2 != None:
			value = max_sessions
			print("Value:", value, "Price:", config["selection"]["price"])
			config["value"] = -float(value)/config["selection"]["price"]
			return config
		else:
			config["value"] = None
			return config
	else:
		value = logs[(find.regs[0][0]+41):find.regs[0][1]]
		print("Value:", value, "Price:", config["selection"]["price"])
		config["value"] = -float(value)/config["selection"]["price"]
		return config
		


def sysbench_by_cost(config):
	# This function should take the terraform output and
    # convert it into a single value to be minimized through Bayes
	# Does so by dividing events per second y the price
	logs = config["logs"]

	if logs is None:
		config["value"] = None
		return config

	if type(logs) is dict:
		logs = json.dumps(logs)

	find = re.search(r"events per second\:  [\d.]+", logs)
	if find != None:
		value = logs[(find.regs[0][0]+18):find.regs[0][1]]
		print("Value:", value, "Price:", config["selection"]["price"])
		config["value"] = float(value)/config["selection"]["price"]
		return config
	else:
		config["value"] = None
		return config