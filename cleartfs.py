from python_terraform import Terraform
import os
import json

for directory in os.listdir(os.getcwd()+"/tf_states"):
    tfstate_file = json.load(open("tf_states/"+directory+"/terraform.tfstate"))
    if ("config details" in tfstate_File["modules"]["outputs"]):
        provider = tfstate_file["modules"]["outputs"]["config details"]["value"]["provider"]
        tfstate_path = 'tf_states/' + directory
	    tfvars = "./tfvars.tfvars"
        instance_wkdir = "instance_deploy/" + provider
	    instance_tf = Terraform(working_dir=instance_wkdir)
        instance_tf.init(backend_config={'path':tfstate_path + '/terraform.tfstate'})
        instance_tf.destroy(auto_approve=True)


