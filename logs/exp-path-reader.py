import os
import json
import pandas as pd




for experiment in os.listdir(os.getcwd() + "/spearmint_exps"):
    df = pd.DataFrame(columns=["Job_number", "vCPUs", "Provider", "Category", "Score", "Value", "Timestamp"])
    job_num = 1
    row = 0
    for file in os.listdir(os.getcwd()+f"/spearmint_exps/{experiment}/jobfiles"):
        if ".json" in file:
            file_path = os.getcwd() + f"/spearmint_exps/{experiment}/jobfiles/{file}"
            job_dict = json.load(open(file_path, "r"))
            vCpus = job_dict["params"]["CPU"][0]
            provider = job_dict["params"]["Provider"][0]
            category = job_dict["params"]["Category"][0]
            value = job_dict["value"]
            score = value * job_dict["selection"]["price"]
            timestamp = job_dict["timestamp"]
            df.loc[row] = [job_num, vCpus, provider, category, score, value, timestamp]
            row += 1
            job_num += 1

    df.to_csv(os.getcwd()+f"/spearmint_exps/{experiment}/job_path.csv")
