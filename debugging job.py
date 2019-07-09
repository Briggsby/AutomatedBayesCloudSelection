import os
import numpy
import driver

print(driver.standard_test(1,
 {"selector":['exact_match'],
  "deployer":['fake_deploy'],
  "log_converter":['sysbench_by_cost'],
  "docker_image":['severalnines/sysbench'],
  "vCPUs":numpy.array([1]), "Memory":['1'],
  "StorageType":["EBS"], "Provider":["aws"]
  }))