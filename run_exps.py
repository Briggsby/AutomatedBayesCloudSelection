import os
import spearmint.main as spearmint
from shutil import copy,copytree

for i in range(20):
    spearmint.main(['--driver=local', '--method=GPEIOptChooser',
    '--method-args="noiseless=0, jobstop=6, eistop=0.1"',
    '-w', '--port=37035', '--max-concurrent=3','./config.pb'])

    os.makedirs("logs/spearmint_exps/", exist_ok=True)
    exp_id = len(os.listdir(os.getcwd()+"/logs/spearmint_exps/"))
    path = f"logs/spearmint_exps/{exp_id}"
    os.makdirs(path, exist_ok=True)
    copy("best_job_and_result.txt", f"{path}/best_job_and_result.txt")
    copy("trace.csv", f"{path}/trace.csv")
    copy("config.pb", f"{path}/config.pb")
    copy("config.vars", f"{path}/config.vars")
    copy("tfvars.tfvars", f"{path}/tfvars.tfvars")
    copytree("jobfiles", f"{path}/jobfiles")

    subprocess.call(["./clearoutput"])
