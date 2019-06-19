variable "region" {
  default = "eu-west-2"
}
variable "instance_type" {
  type = "string"
  default = "t2.micro"
}
variable "amis" {
  type = "map"
  default = {
    eu-west-2 = "ami-09ead922c1dad67e4"
  }
}

variable "access_key" {
  default = "default_key"
}