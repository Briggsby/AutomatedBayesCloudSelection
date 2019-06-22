cd ../docker_deploy
terraform destroy -auto-approve
cd ../instance_deploy/$1
terraform destroy -auto-approve
