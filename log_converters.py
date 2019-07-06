import re
import json

def sysbench_by_cost(config):
	# This function should take the terraform output and
    # convert it into a single value to be minimized through Bayes
	# Does so by dividing events per second y the price
	logs = json.dumps(config["logs"])
	find = re.search(r"events per second\:  [\d.]+", logs)
	if find != None:
		value = logs[(find.regs[0][0]+18):find.regs[0][1]]
		print("Value:", value, "Price:", config["selection"]["price"])
		config["value"] = float(value)/config["selection"]["price"]
		return config
	else:
		config["value"] = None
		return config