import os
import example

print(example.standard_test(1,
 {"selector":['exact_match'],
  "deployer":['fake_deploy'],
  "log_converter":['sysbench_by_cost'],
  "vCPUs":[1], "Memory":['1'],
  "StorageType":["EBS"], "Provider":["aws"]
  }))