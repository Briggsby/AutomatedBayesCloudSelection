cd docker_deploy
terraform destroy -auto-approve
cd ../instance_deploy/aws
terraform destroy -auto-approve