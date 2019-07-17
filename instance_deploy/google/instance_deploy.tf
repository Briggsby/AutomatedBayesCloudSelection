terraform {
  backend "local" {}
}

provider "google" {
  credentials = "${file("./credentials/account.json")}"
  project     = "${var.google_project_id}"
  region      = "${var.google_region}"
}

resource "random_string" "random_firewall_name" {
  length = 16
  upper = false
  number = false
  special = false
}

resource "random_string" "random_instance_name" {
  length = 16
  upper = false
  number = false
  special = false
}

resource "google_compute_firewall" "docker_access" {
  name = "${random_string.random_firewall_name.result}"
  network = "default"
  description = "Allow docker access"
  # To keep it simple, we allow incoming requests from any IP. In future, we need to 
  # lock this down to just the IPs of trusted servers (e.g., of a load balancer).

  # TCP port 2376 for remote docker api
  allow {
    protocol  = "tcp"
    ports = ["2376"]
  }
  # HTTP
  allow {
    protocol = "tcp"
    ports = ["8000"]
  }
  # Docker metrics api
  allow {
    protocol = "tcp"
    ports = ["9323"]
  }
  target_tags = ["docker-host"]
}

resource "google_compute_instance" "docker_host" {
  name = "${random_string.random_instance_name.result}"
  machine_type = "${var.instance_type}"
  zone = "${var.google_zone}"
  tags = ["docker-host"]

  network_interface {
    network = "projects/${var.google_project_id}/global/networks/default"
    access_config {
      // Ephemeral IP
    }
  }

  boot_disk {
    initialize_params {
      image = "${var.google_image}"
    }
  }

  connection {
    type = "ssh"
    host = "${self.network_interface.0.access_config.0.nat_ip}"
    user = "${var.google_username}"
    private_key = "${file("./credentials/${var.google_access_key}")}"
  }

  provisioner "file" {
    source      = "../files/google_docker.service"
    destination = "docker.service"
  }
  # update for remote dockerd metrics API
  provisioner "file" {
    source      = "../files/daemon.json"
    destination = "daemon.json"
  }
  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update -y",
      "sudo apt-get install curl -y",
      "sudo curl -fsSL https://get.docker.com -o get-docker.sh",
      "sudo sh get-docker.sh",
      "sudo cp docker.service /lib/systemd/system/docker.service",
      "sudo mkdir -p /etc/docker/",
      "sudo cp daemon.json /etc/docker/daemon.json",
      "sudo systemctl daemon-reload",
      "sudo systemctl restart docker"
    ]
  }
}

output "docker_host_ip" {
  value = "${google_compute_instance.docker_host.network_interface.0.access_config.0.nat_ip}"
}

output "config_details" {
  value = {provider = "google", instance_type = "${var.instance_type}"}
}
