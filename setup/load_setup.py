import logging
from logging.config import dictConfig
import json
import os

#-------------------------------------------------------------------
def load_setup(check_folds, load_logs):
    if 'true' in check_folds.lower():
        check_folders()
    else:
        print("\nNot Checking Folders")
    if 'true' in load_logs.lower():
        load_loggers()
    else:
        print("\nNot Loading Loggers")
    
    print()
#-------------------------------------------------------------------

#-------------------------------------------------------------------
def load_loggers():
    print("\nLoggers Loading ...")
    try:
        with open("log_config.json", 'r') as f:
            log_config_data = json.load(f)
            dictConfig(log_config_data)
    except FileNotFoundError:
        with open("logging_config.json", 'r') as f:
            log_config_data = json.load(f)

    print("Loggers Loaded:")
    for logger_name in log_config_data['loggers']:
        print(f"\t{logger_name}")
#-------------------------------------------------------------------

#-------------------------------------------------------------------
def check_folders():
    cwd = os.path.join(os.getcwd())
    paths = {'logs': os.path.join(cwd, "logs"),
             'temp': os.path.join(cwd, "temp"),
             'cach': os.path.join(cwd, "cache"),}

    print("\nChecking Folders...")
    for key in paths.keys():
        if not os.path.exists(paths[key]):
            os.mkdir(paths[key])
            print(f"Folder Created : {key}")
        else:
            print(f"Folder Exists  : {key}")
    print()
#-------------------------------------------------------------------
