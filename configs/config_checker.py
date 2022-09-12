import logging
import configparser
import os

__logger = logging.getLogger("main").getChild(__name__)

#-----------------------------------------------------------------------------------------------------------
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
            # non_existing_configs.append(f"configs//{obj}.ini")
            non_existing_configs.append(os.path.join(os.getcwd(), 'configs', f'{obj}.ini'))
            create_config(config_fp)
            
    return non_existing_configs
#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
def create_config(path, dict_to_write=None):
    config_writer = configparser.ConfigParser()
    config_writer.optionxform = str
    if not dict_to_write:
        config_writer['DEFAULT'] = {"Minimum_Fields": "Example,Fields", "Additional_Fields": "More,Examples"}
    else:
        config_writer['DEFAULT'] = dict_to_write
    with open(path, 'w+') as configfile:
        config_writer.write(configfile)
#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
def get_user_configs():
    config_reader = configparser.ConfigParser()
    user_ini = os.path.join(os.getcwd(), "configs", "user.ini")
    config_reader.read_file(open(user_ini))

    user_config = {}
    # user_config['org_env'] = config_reader.get("DEFAULT", "Org_Env")
    user_config['dst_env'] = config_reader.get("DEFAULT", "DEST_Org_Name")
    user_config['src_env'] = config_reader.get("DEFAULT", "SRCE_Org_Name")
    # user_config['obj_list'] = config_reader.get("DEFAULT", "Object_List").split(',')
    user_config['obj_list'] = get_WHERE_fields(
                    config_reader.get("DEFAULT", "Object_List").split(','))
    
    return user_config
#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
def get_WHERE_fields(obj_list):
    config_reader = configparser.ConfigParser()
    all_obj_items = {}
    __logger.info(f"Getting WHERE fields and generating queries from configs. ")
    for obj in obj_list:
        user_ini = os.path.join(os.getcwd(), "configs", f"{obj}.ini")
        config_reader.read_file(open(user_ini))

        min_fields = config_reader.get("DEFAULT", "Minimum_Fields").split(',')
        add_fields = config_reader.get("DEFAULT", "Additional_Fields").split(',')

        all_obj_items[obj] = {"min_fields": min_fields, "add_fields": add_fields}
    
    return all_obj_items
#-----------------------------------------------------------------------------------------------------------
