import json
from shutil import copy
import pandas as pd
import os
import datetime


def cloudsuite():
    df = pd.DataFrame(columns=['instance', 'throughput', 'cpu', 'type', 'provider', 'price', 'value'])

    all_logs = json.load(open("fulllogs.json", "r"))
    row = 0
    for i in all_logs:
        if (type(all_logs[i]) is dict):
            if ('value' in all_logs[i] and all_logs[i]['value'] is not None and
            'vars' in all_logs[i]):
                if ('Maximum limit for number of sessions too low' not in all_logs[i]['logs']):
                    if (all_logs[i]['vars']['log_converter'] == 'cloudsuite_media_stream' and
                    all_logs[i]['vars']['deployer'] == 'vm_cloudsuite3_media_deploy'):
                        value = abs(all_logs[i]['value'])
                        price = all_logs[i]['selection']['price']
                        throughput = value*price
                        instance = all_logs[i]['selection']['instance']
                        cpu = all_logs[i]['params']['CPU']
                        provider = all_logs[i]['params']['Provider']
                        category = all_logs[i]['params']['Category']
                        df.loc[row] = [instance, throughput, cpu, category, provider, price, value]
                        row += 1
                        print(value, price, throughput, instance)

    print(df)
    df.to_csv("cloudsuite_results.csv")


def vbench():
    df = pd.DataFrame(columns=['instance', 'score', 'cpu', 'type', 'provider', 'price', 'value', 'type', 'filter'])

    all_logs = json.load(open("fulllogs.json", "r"))
    row = 0
    for i in all_logs:
        if (type(all_logs[i]) is dict):
            if ('value' in all_logs[i] and all_logs[i]['value'] is not None and
            'vars' in all_logs[i]):
                if ('Maximum limit for number of sessions too low' not in all_logs[i]['logs']):
                    if (all_logs[i]['vars']['log_converter'] == 'vbench' and
                    all_logs[i]['vars']['deployer'] == 'vbench'):
                        vbench_filter = all_logs[i]["vars"]["vbench_filter"]
                        vbench_category = all_logs[i]["vars"]["vbench_type"]
                        if vbench_filter == "house" and vbench_category == "vod":
                            value = abs(all_logs[i]['value'])
                            price = all_logs[i]['selection']['price']
                            score = value*price
                            instance = all_logs[i]['selection']['instance']
                            cpu = all_logs[i]['params']['CPU']
                            provider = all_logs[i]['params']['Provider']
                            category = all_logs[i]['params']['Category']
                            df.loc[row] = [instance, score, cpu, category, provider, price, value, vbench_category, vbench_filter]
                            row += 1
                            print(value, price, score, instance)

    print(df)
    df.to_csv("vbench_results.csv")

def curltest():
    df = pd.DataFrame(columns=['instance', 'score', 'cpu', 'type', 'provider', 'price', 'value'])

    all_logs = json.load(open("fulllogs.json", "r"))
    row = 0
    for i in all_logs:
        if (type(all_logs[i]) is dict):
            if ('value' in all_logs[i] and all_logs[i]['value'] is not None and
            'vars' in all_logs[i]):
                if ('20190719' in all_logs[i]['timestamp']):
                    if (all_logs[i]['vars']['log_converter'] == 'ping_testserver' and
                    all_logs[i]['vars']['deployer'] == 'ping_testserver'):
                        value = abs(all_logs[i]['value'])
                        price = all_logs[i]['selection']['price']
                        avg_delay = value*price
                        instance = all_logs[i]['selection']['instance']
                        cpu = all_logs[i]['params']['CPU']
                        provider = all_logs[i]['params']['Provider']
                        category = all_logs[i]['params']['Category']
                        df.loc[row] = [instance, avg_delay, cpu, category, provider, price, value]
                        row += 1
                        print(value, price, avg_delay, instance)

    print(df)
    df.to_csv("curltest_results.csv")


def exps():
    df = pd.DataFrame(columns=['ID', 'Selector', 'Deployer', 'Interpreter', 'Concurrent_Jobs', 'Multiple_Providers', 'Jobs_completed', 'Best_instance', 'Best_CPU', 'Best_Provider', 'Best_Category', 'Best_JobID', 'Best_Result', "Time", "Cost"])
    row = 0
    for directory in os.listdir(os.getcwd()+"/spearmint_exps"):
        selector = "exact_match"
        best_results_file = open("spearmint_exps/"+directory+"/best_job_and_result.txt", "r").read().splitlines()

        jobs_completed = len(os.listdir(os.getcwd()+"/spearmint_exps/"+directory+"/jobfiles"))

        deployer = "vbench"
        interpreter = "vbench"

        for idx, line in enumerate(best_results_file):
            split = line.split(":")
            if idx == 0:
                    best_result = float(split[1])
            elif idx == 1:
                    best_jobid = split[1].strip(" ")
            elif idx == 4:
                    best_cpu = int(split[1].strip(' "'))
            elif idx == 6:
                    best_provider = split[1].strip(' "')
            elif idx == 8:
                    best_category = split[1].strip(' "')
        if int(directory) < 20:
            concurrent_jobs = 3
            multiple_providers = True
        elif int(directory) < 40:
            concurrent_jobs = 3
            multiple_providers = False    
        elif int(directory) < 50:
            concurrent_jobs = 1
            multiple_providers = True  
        elif int(directory) < 60:       
            deployer = "ping_testserver"
            interpreter = "ping_testserver"
            concurrent_jobs = 1
            multiple_providers = True
        elif int(directory) < 70:
            concurrent_jobs = 1
            multiple_providers = True  
        elif int(directory) < 90:
            concurrent_jobs = 2
            multiple_providers = True
        else:
            concurrent_jobs = 1
            multiple_providers = False

        time, cost = get_time_and_cost(os.getcwd()+"/spearmint_exps/"+directory)            

        best_jobfile = open(os.getcwd()+"/spearmint_exps/"+directory+"/jobfiles/"+best_jobid+".json", "r")
        instance_type = json.load(best_jobfile)["selection"]["instance"]
        df.loc[row] = [directory, selector, deployer, interpreter, concurrent_jobs, multiple_providers, jobs_completed, instance_type, best_cpu, best_provider, best_category, best_jobid, best_result, time, cost]
        row += 1

    print(df)
    df.to_csv("exps_results.csv")


def get_time_and_cost(experiment_folder):
    job_path_df = pd.read_csv(experiment_folder+"/job_path.csv")
    price = sum([job_path_df.loc[i,"Price"] for i in job_path_df.index])
    times = [datetime.datetime.strptime(str(i), '%Y%m%d%H%M%S') for i in job_path_df["Timestamp"]]
    time = max(times) - min(times)
    time = time.seconds
    return time, price

copy("fulllogs.json", "backup.json")
cloudsuite()
vbench()
curltest()
exps()