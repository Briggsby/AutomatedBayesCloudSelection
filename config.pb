language: PYTHON
name: "driver"

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
 # options: "google"
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
