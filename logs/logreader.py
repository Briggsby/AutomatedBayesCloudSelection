import json
from shutil import copy
import pandas as pd


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


copy("fulllogs.json", "backup.json")
cloudsuite()
vbench()