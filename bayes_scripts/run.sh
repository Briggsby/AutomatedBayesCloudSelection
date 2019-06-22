cd ../docker_deploy
rm terraform.tfstate
rm terraform.tfstate.backup
cd ../instance_deploy/$1
terraform init
terraform apply -auto-approve
cd ../../docker_deploy
terraform init
terraform apply -auto-approve
terraform output -json > ../logs/newestlogs.json
cd ../logs/
touch newestlogs.json
jq -s '.[1] + { ((.[1]|length)|tostring) :.[0]}' newestlogs.json fulllogs.json > temp.json
mv temp.json fulllogs.json
