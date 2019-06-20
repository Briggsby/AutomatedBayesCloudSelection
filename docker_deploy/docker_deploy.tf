data "terraform_remote_state" "state" {
  backend = "local"
  config = {
    path = "../instance_deploy/terraform.tfstate"
  }
}

# Configure Docker provider and connect to the local Docker socket
provider "docker" {
#  For local runs
#  host = "unix:///var/run/docker.sock"
  host = "tcp://${data.terraform_remote_state.state.docker_host_ip}:2376"
  # version = "1.1.1"
}

resource "docker_image" "image" {
  name = "${var.image}:${var.image_version}"
}

resource "docker_container" "container" {
  image = "${docker_image.image.latest}"
  name  = "${var.container_name}"
  ports {
    internal = 80
    external = 8000
  }
  entrypoint = "${var.entrypoint}"
  command = "${var.commands}"
  attach = true
  must_run = false
  logs = true
}

output "config_details" {
  value = "${data.terraform_remote_state.state.config_details}"
}

output "timestamp" {
  value = "${timestamp()}"
}

output "docker_logs" {
  value = "${docker_container.container.container_logs}"
}