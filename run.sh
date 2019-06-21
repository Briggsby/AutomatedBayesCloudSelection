cd docker_deploy
rm terraform.tfstate
rm terraform.tfstate.backup
cd ../instance_deploy/aws
terraform init
terraform apply -auto-approve
cd ../../docker_deploy
terraform init
terraform apply -auto-approve
terraform output -json > ../newlogs.json
cd ../
touch logs.json
jq -s '.[1] + { ((.[1]|length)|tostring) :.[0]}' newlogs.json logs.json > temp.json
mv temp.json logs.json