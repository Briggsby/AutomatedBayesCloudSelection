variable "google_region" {
  default = "eu-west2"
}

variable "google_project_id" {
  default = "my-project-id"
}

variable "instance_type" {
  type = "string"
  default = "t2.micro"
}

variable "tfstate_path" {
  type = "string"
  default = ".."
}