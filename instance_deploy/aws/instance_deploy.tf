terraform {
  backend "local" {}
}

provider "aws" {
  shared_credentials_file = "./credentials/aws_credentials"
  region     = "${var.aws_region}"
}

resource "aws_security_group" "access" {
  name_prefix = "docker_host"
  description = "Allow SSH inbound, http, docker host, and all outbound traffic"
  # To keep it simple, we allow incoming HTTP requests from any IP. In future, we need to 
  # lock this down to just the IPs of trusted servers (e.g., of a load balancer).
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
 # TCP port 2376 for remote docker api
  ingress {
    from_port = 2376
    to_port   = 2376
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
 # TCP 9323 for docker metrics api
 ingress {
    from_port = 9323
    to_port   = 9323
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
 # TCP 9090 for Prometheus
 ingress {
    from_port = 9090
    to_port   = 9090
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
 # Http
  ingress {
    from_port = 8000
    to_port   = 8000
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
 # allow any outbound  traffic
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "docker_host" {
  instance_type = "${var.instance_type}"
  ami = "${var.aws_amis[var.aws_region]}"

  tags = {Name = "docker_host"}
  vpc_security_group_ids = ["${aws_security_group.access.id}"]
  key_name = "${var.aws_access_key}"

  root_block_device = {
    volume_size = 15
  }

  connection {
    type = "ssh"
    host = "${self.public_ip}"
    user = "ec2-user"
    private_key = "${file("./credentials/${var.aws_access_key}.pem")}"
  }

  # update for remote dockerd API
  provisioner "file" {
    source      = "../files/docker.service"
    destination = "docker.service"
  }
  # update for remote dockerd metrics API
  provisioner "file" {
    source      = "../files/daemon.json"
    destination = "daemon.json"
  }
  provisioner "remote-exec" {
    inline = [
      "sudo yum update -y",
      "sudo amazon-linux-extras install docker -y",
      "sudo cp docker.service /lib/systemd/system/docker.service",
      "sudo cp daemon.json /etc/docker/daemon.json",
      "sudo systemctl daemon-reload",
      "sudo systemctl restart docker"
    ]
  }
}
output "docker_host_ip" {
  value = "${aws_instance.docker_host.public_ip}"
}

output "config_details" {
  value = {provider = "aws", instance_type = "${var.instance_type}"}
}
