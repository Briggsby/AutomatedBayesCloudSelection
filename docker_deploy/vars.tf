variable "image" {
    default = "severalnines/sysbench"
    # default = "nginx"
}

variable "image_version" {
    default = "latest"
}

variable "container_name" {
    default = "sysbench"
}

variable "entrypoint" {
    type = "list"
    default = ["sysbench"]
}

variable "commands" {
    type = "list"
    default = ["--test=cpu", "--cpu-max-prime=5000", "run"]
    # default = []
}