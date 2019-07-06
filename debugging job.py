import os
import example

print(example.standard_test(1,
 {"selector":['exact_match'],
  "deployer":['vm_docker_deploy_old'],
  "log_converter":['sysbench_by_cost'],
  "vCPUs":[1], "Memory":['1'],
  "StorageType":["EBS"], "Provider":["aws"]
  }))