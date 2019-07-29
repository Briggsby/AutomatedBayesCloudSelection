from python_terraform import Terraform
import os
import json
import time

base_dir = os.path.dirname(os.path.realpath(__file__))

print("Sleeping for 30 to give time for leftover terraform processes")
time.sleep(30) # Give enough time for any leftover instace provisioning process to get to a stoppable point
# Prevents hangs, may be a cleaner way of doing this I am unaware of

for directory in os.listdir(os.getcwd()+"/tf_states"):
        tfstate_file = json.load(open("tf_states/"+directory+"/terraform.tfstate"))
        if ("config_details" in tfstate_file["modules"][0]["outputs"]):
                instance_type = tfstate_file['modules'][0]['outputs']['config_details']['value']['instance_type']
                print(f'Removing {instance_type}')
                provider = tfstate_file["modules"][0]["outputs"]["config_details"]["value"]["provider"]
                tfstate_path = base_dir+ '/tf_states/' + directory
                tfvars = base_dir + "/tfvars.tfvars"
                instance_wkdir = base_dir + "/instance_deploy/" + provider
                instance_tf = Terraform(working_dir=instance_wkdir)
                instance_tf.init(backend_config={'path':tfstate_path + '/terraform.tfstate'})
                destroy = instance_tf.destroy(auto_approve=True, var_file=base_dir+"/tfvars.tfvars")
                print(destroy)
                


