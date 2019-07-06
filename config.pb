language: PYTHON
name: "driver"

# THESE 3 ENUMS ARE USED TO DECIDE FUNCTIONS USED
# THEY SHOULD ONLY HAVE ONE OPTION
# (unless you are intentionally somehow seeing,
# for example, which selector works better)
# For available functions, see the python scripts

variable {
 name: "selector"
 type: ENUM
 size: 1
 options: 'exact_match'
}

variable {
 name: "deployer"
 type: ENUM
 size: 1
 options: 'fake_deploy'
}

variable {
 name: "log_converter"
 type: ENUM
 size: 1
 options: 'sysbench_by_cost'
}

# You can use similar enums for specific modules,
# such as to specify a docker_image
variable {
 name: "docker_image"
 type: ENUM
 size: 1
 options: 'severalnines/sysbench'
}

# Variables from this point are are those
# used by the selector function to pick
# the appropriate configuration

variable {
 name: "vCPUs"
 type: INT
 size: 1
 min: 1
 max: 2
}

variable {
 name: "Memory"
 type: ENUM
 size: 1
 options: '0.5'
 options: '1'
 options: '2'
 options: '4'
 options: '8'
 options: '16'
}

variable {
 name: "StorageType"
 type: ENUM
 size: 1
 options: "EBS"
 options: "SSD"
}

variable {
 name: "Provider"
 type: ENUM
 size: 1
 options: "aws"
}


# Example variable
#
# variable {
#  name: "vCPU"
#  type: INT
#  size: 1
#  min: 1
#  max: 16
# }
#
# For a float, use type: FLOAT
#
# Enumeration example
# 
# variable {
#  name: "Category"
#  type: ENUM
#  size: 1
#  options: "General"
#  options: "Memory"
#  options: "Compute"
#  options: "Accelerated"
#  options: "Storage"
# }
