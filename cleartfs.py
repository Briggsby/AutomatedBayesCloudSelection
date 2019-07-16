from python_terraform import Terraform
import os
import json

base_dir = os.path.dirname(os.path.realpath(__file__))

for directory in os.listdir(os.getcwd()+"/tf_states"):
        tfstate_file = json.load(open("tf_states/"+directory+"/terraform.tfstate"))
        if ("config_details" in tfstate_file["modules"][0]["outputs"]):
                print(f'Removing {tfstate_file["modules"][0]["outputs"]["config_details"]["value"]["instance_type"]}')
                provider = tfstate_file["modules"][0]["outputs"]["config_details"]["value"]["provider"]
                tfstate_path = base_dir+ '/tf_states/' + directory
                tfvars = base_dir + "/tfvars.tfvars"
                instance_wkdir = base_dir + "/instance_deploy/" + provider
                instance_tf = Terraform(working_dir=instance_wkdir)
                instance_tf.init(backend_config={'path':tfstate_path + '/terraform.tfstate'})
                destroy = instance_tf.destroy(auto_approve=True)
                print(destroy)
                


