def instance_test(params):
	# Find instance these params suggest should be tested
	# Run test on that instance, get its logs
	# Convert logs into quantitative value
	# Return that value
	pass
	return 1


def main(job_id, params):
	print 'Anything printed here will end up in the output directory for job #:', str(job_id)
	print params
	return instance_test(params)



