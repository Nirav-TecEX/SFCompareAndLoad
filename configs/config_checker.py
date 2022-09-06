import logging
import configparser
import os

__logger = logging.getLogger("main").getChild("config_checker")

def check_configs_exist():
    __logger.info("Checking config files... ")

    config_reader = configparser.ConfigParser()
    user_ini = os.path.join(os.getcwd(), "configs", "user.ini")
    config_reader.read_file(open(user_ini))

    obj_list = config_reader.get("DEFAULT", "Object_List").split(',')

    non_existing_configs = []
    for obj in obj_list:
        __logger.info(f"Checking configs\{obj}.ini")
        config_fp = os.path.join(os.getcwd(), "configs", f"{obj}.ini")
        if not os.path.exists(config_fp):
            non_existing_configs.append(f"configs//{obj}.ini")
            create_config(config_fp)
            
    return non_existing_configs

def create_config(path):
    config_writer = configparser.ConfigParser()
    config_writer['DEFAULT'] = {"Matching_Fields": "Example,Fields"}
    with open(path, 'w') as configfile:
        config_writer.write(configfile)
