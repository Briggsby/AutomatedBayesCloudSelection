import re as re

def sysbench_to_costpercycles(logs):
	find = re.search(r"events per second\:  [\d.]+", logs)
	if find != None:
		value = logs[(find.regs[0][0]+18):find.regs[0][1]]
		return float(value)
	else:
		return 0


def main(params, job_id, logs, price):
	# This function should take the terraform output and
    # convert it into a single value to be minimized through Bayes
	return sysbench_to_costpercycles(logs)