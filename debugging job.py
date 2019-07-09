import os
import numpy
import driver

print(driver.standard_test(1,
 {"vCPUs":numpy.array([1]), "Memory":['1'],
  "StorageType":["EBS"], "Provider":["aws"]
  }))