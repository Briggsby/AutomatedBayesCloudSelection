import os
from shutil import copy,copytree

os.makedirs("logs/spearmint_exps/", exist_ok=True)
exp_id = len(os.listdir(os.getcwd()+"/logs/spearmint_exps/"))
path = f"logs/spearmint_exps/{exp_id}"
os.makedirs(path, exist_ok=True)
copy("best_job_and_result.txt", f"{path}/best_job_and_result.txt")
copy("trace.csv", f"{path}/trace.csv")
copy("config.pb", f"{path}/config.pb")
copy("config.vars", f"{path}/config.vars")
copy("tfvars.tfvars", f"{path}/tfvars.tfvars")
copytree("jobfiles", f"{path}/jobfiles")
if os.path.isfile("command.txt"):
    copy("command.txt", f"{path}/command.txt")