variable "image" {
    # default = "severalnines/sysbench"
    default = "nginx"
}

variable "image_version" {
    default = "latest"
}

variable "container_name" {
    default = "nginx"
}

variable "commands" {
    type = "list"
    # default = ["sysbench", "--test=cpu", "--cpu-max-prime=10000", "run"]
    default = []
}