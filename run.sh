cd docker_deploy
rm terraform.tfstate
rm terraform.tfstate.backup
cd ../instance_deploy/aws
terraform init
terraform apply -auto-approve
cd ../../docker_deploy
terraform init
terraform apply -auto-approve
