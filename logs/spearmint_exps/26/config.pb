language: PYTHON
name: "abcs_driver"

# Variables from this point are are those
# used by the selector function to pick
# the appropriate configuration

variable {
 name: "CPU"
 type: ENUM
 size: 1
 options: '2'
 options: '4'
 options: '8'
}

variable {
 name: "Provider"
 type: ENUM
 size: 1
 #  options: "aws"
 options: "google"
}

variable {
 name: "Category"
 type: ENUM
 size: 1
 options: "General"
 options: "Memory"
 options: "CPU"
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
