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
            non_existing_configs.append(os.path.join(os.getcwd(), 'configs', f'{obj}.ini'))
            create_config(config_fp)
            
    return non_existing_configs
#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
def get_obj_min_fields(obj_name, user_config):
    non_existing_configs = []
    
    __logger.info(f"Checking configs\{obj_name}.ini")
    config_fp = os.path.join(os.getcwd(), "configs", f"{obj_name}.ini")
    if not os.path.exists(config_fp):
        non_existing_configs.append(os.path.join('configs', f'{obj_name}.ini'))
        create_config(config_fp)

        with open(os.path.join(os.getcwd(), "CONFIGS_TO_ADD.txt"), 'a') as f:
            f.write(f"{obj_name}")
            for configName in non_existing_configs:
                f.write("\t"+configName+"\n")
            f.write("\n")
        return user_config
    else:
        user_config['obj_list'][obj_name] = get_WHERE_fields_for_obj([obj_name])

    return user_config
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
def get_user_configs(dst_org):
    user_config = {}
    # user_config['org_env'] = config_reader.get("DEFAULT", "Org_Env")
    user_config['dst_env'] = dst_org
    user_config['src_env'] = 'temp'
    user_config['obj_list'] = ''
    
    return user_config
#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
def get_WHERE_fields(obj_list):
    config_reader = configparser.ConfigParser()
    all_obj_items = {}
    __logger.debug(f"Getting WHERE fields and generating queries from configs. ")
    for obj in obj_list:
        user_ini = os.path.join(os.getcwd(), "configs", f"{obj}.ini")
        config_reader.read_file(open(user_ini))

        min_fields = config_reader.get("DEFAULT", "Minimum_Fields").split(',')
        add_fields = config_reader.get("DEFAULT", "Additional_Fields").split(',')

        all_obj_items[obj] = {"min_fields": min_fields, "add_fields": add_fields}
    
    return all_obj_items
#-----------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------
def get_WHERE_fields_for_obj(obj_list):
    config_reader = configparser.ConfigParser()
    all_obj_items = {}
    __logger.debug(f"Getting WHERE fields and generating queries from configs for {obj_list}. ")
    for obj in obj_list:
        user_ini = os.path.join(os.getcwd(), "configs", f"{obj}.ini")
        config_reader.read_file(open(user_ini))

        min_fields = config_reader.get("DEFAULT", "Minimum_Fields").split(',')
        add_fields = config_reader.get("DEFAULT", "Additional_Fields").split(',')

        all_obj_items = {"min_fields": min_fields, "add_fields": add_fields}
    
    return all_obj_items
#-----------------------------------------------------------------------------------------------------------
