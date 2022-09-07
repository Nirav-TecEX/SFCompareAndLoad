import logging
import configparser
import os

__logger = logging.getLogger("main").getChild("config_checker")

def check_configs_exist():
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
    config_writer.optionxform = str
    config_writer['DEFAULT'] = {"Minimum_Fields": "Example,Fields", "Additional_Fields": "More,Examples"}
    with open(path, 'w') as configfile:
        config_writer.write(configfile)

def get_user_configs():
    config_reader = configparser.ConfigParser()
    user_ini = os.path.join(os.getcwd(), "configs", "user.ini")
    config_reader.read_file(open(user_ini))

    user_config = {}
    user_config['org_env'] = config_reader.get("DEFAULT", "Org_Env")
    user_config['dst_env'] = config_reader.get("DEFAULT", "DEST_Org_Name")
    user_config['src_env'] = config_reader.get("DEFAULT", "SRCE_Org_Name")
    user_config['obj_list'] = config_reader.get("DEFAULT", "Object_List").split(',')
    
    return user_config
