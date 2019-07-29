variable "google_region" {
  default = "europe-west2"
}

variable "google_zone" {
  default = "europe-west2-c"
}

variable "google_project_id" {
  default = "my-project-id"
}

variable "google_username" {
  default = "my_username"
}

variable "google_access_key" {
  default = "defaultkey"
}

variable "google_image" {
  default = "debian-cloud/debian-9"
}

variable "instance_type" {
  type = "string"
  default = "f1-micro"
}

variable "tfstate_path" {
  type = "string"
  default = ".."
}
