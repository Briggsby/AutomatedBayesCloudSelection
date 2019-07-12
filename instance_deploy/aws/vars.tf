variable "aws_region" {
  default = "eu-west-2"
}

variable "instance_type" {
  type = "string"
  default = "t2.micro"
}

variable "tfstate_path" {
  type = "string"
  default = ".."
}

variable "aws_amis" {
  type = "map"
  default = {
    eu-west-2 = "ami-0d8e27447ec2c8410"
  }
}

variable "aws_access_key" {
  default = "default_key"
}