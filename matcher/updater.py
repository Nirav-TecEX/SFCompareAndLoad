import logging
import os
import pandas as pd
import json
import time

from .setup import update_details
from .salesforce import ComplexSF
from configs.config_checker import create_config, sf_Module_path

__logger = logging.getLogger("matcher").getChild(__name__)

# ---------------------------------------------------------------------------------------------------------
def update_single_obj_cache(org_type, org_name, obj_name, user_config, env_vars):
    """ This function should check the necessary destination and source orgs for the objs and update the 
        required file as needed. 
        
        It will update if the last update was not performed within the last 7 days. 

        This function calls the 'create_query_strs' function in order to create the query for SalesForce
        and the matching string using data from the configs. It then saves the output/ updates to the 
        cache.  

        param :: org_type             accepts either 'src' or 'dst'
        param :: org_name             'org': 'tecex--ruleseng'
        param :: obj_name             name of the object to check for 'name': 'cpa'
        param :: user_config          takes the data read from the user_config to know which orgs to check 
                                      for recently updated time.
        
        Still need to implement the timer checker. """
    
    obj_path = os.path.join(sf_Module_path(), 'cache', org_name, f"{obj_name}.xlsx")
    if 'true' in env_vars("DEBUG_MODE").lower(): 
        time_interval = int(env_vars("debug_update_interval"))
    else:
        time_interval = int(env_vars("update_interval"))
    
    __logger.debug(f"Checking if last update was less than {time_interval/60/60/24} days ago.")
    try:
        if should_not_update_file(obj_path, time_interval):
            __logger.debug(f"ALREADY UPDATED {obj_path}")
            return 0
    except FileNotFoundError as e:
        return 1  
        # create_config(os.path.join(os.getcwd(), "configs", f"{obj_name}.ini"))
    
    __logger.info(f"Attempting to update cache for {obj_path.split('cache')[1]}.")
    objs = {}
    objs['obj_list'] = {}
    objs['obj_list'][obj_name] = user_config['obj_list'][obj_name]

    __logger.debug(f"Creating queries for updates ")
    dict_of_query_strs = create_query_strs(objs['obj_list'])
    __logger.debug("Queries:")
    for key in dict_of_query_strs:
        __logger.debug(f"\t {dict_of_query_strs[key]}")

    if 'src' in org_type:
        user_config = update_login_details(user_config, env_vars, org_name)
        sf = ComplexSF(org_name,
                    user_config[f'{org_type}_details'][org_name]['username'],
                    user_config[f'{org_type}_details'][org_name]['password'],
                    user_config[f'{org_type}_details'][org_name]['token'])
    
    else: 
        sf = ComplexSF(user_config[f'{org_type}_env'],
                    user_config[f'{org_type}_details']['username'],
                    user_config[f'{org_type}_details']['password'],
                    user_config[f'{org_type}_details']['token']) # sandbox=user_config['dst_env']

    for obj_key in dict_of_query_strs:
        __logger.debug(f"Performing query: {dict_of_query_strs[obj_key]}")

        if 'example, fields' in dict_of_query_strs[obj_key].lower():
            continue
        
        records = sf.perform_query(dict_of_query_strs[obj_key])
        __logger.debug(f"Creating match string for {obj_key}")
        records_with_match_str = create_match_string(records, obj_key)

        save_records(records_with_match_str,
                        obj_key, 
                        org_name,
                        sf)
    
    return 0
# ---------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------
def create_query_strs(obj_list):
    dict_of_query_strs = {}
    for obj_name in obj_list:
        if not 'Id' in obj_list[obj_name]['min_fields']:
            obj_list[obj_name]['min_fields'].insert(0, 'Id')
        selections = ', '.join(obj_list[obj_name]['min_fields'])
        query_str = f"SELECT {selections} FROM {obj_name}"
        dict_of_query_strs[obj_name] = query_str
        
    return dict_of_query_strs
# ---------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------
def create_match_string(records, obj_key):
    records_with_match_str = []
    for record in records:
        match_str = ''
        for attribute in record.keys():
            if attribute != 'attributes' and attribute != 'Id':
                if record[attribute]:
                    attr_str = record[attribute]
                else:
                    attr_str = ''
                match_str = match_str + f"[{attr_str}]"
        match_str = match_str + f"@{obj_key}"
        record["Matching String"] = match_str
        records_with_match_str.append(record)
    return records_with_match_str
# ---------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------
def save_records(records, obj, dst_env, sfObj: ComplexSF):
    path = os.path.join(sf_Module_path(), 'cache', f'{dst_env}')
    excel_path = os.path.join(path, f"{obj}.xlsx")
    __logger.debug(f"Saving to: {excel_path} ")
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        df = pd.DataFrame.from_dict(records)
        df.to_excel(writer)
# ---------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------
def save_records_to_json(records, obj, dst_env, sfObj: ComplexSF):
    path = os.path.join(sf_Module_path(), 'cache', f'{dst_env}')
    json_path = os.path.join(path, f"{obj}.json")
    __logger.debug(f"Saving to: {json_path} ")
    with open(json_path, 'w+') as outstream:
        outstream.write(json.dumps(records, indent = 4))
# ---------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------
def update_id_to_obj_mapper(saving_path, sf: ComplexSF):
    __logger.info("Updating mapper which maps Ids to Objects. ")

    all_objects = sf.describe()['sobjects']
    prefix_dict = {all_objects[i]['keyPrefix'] : all_objects[i]['name'] for i in range(len(all_objects))}

    __logger.info(f"Saving to {saving_path}")
    with open(saving_path, 'w+') as outstream:
        outstream.write(json.dumps(prefix_dict, indent = 4))
# ---------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------
def update_login_details(user_config, env_vars, org_name):
    try:
        if org_name in user_config['src_details'].keys():
            return
    except AttributeError as e:
        pass

    return update_details('src_env', user_config, env_vars, org_name)
# ---------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------
def should_not_update_file(path, time_interval):
        return time_interval > time.time() - os.path.getmtime(path)
# ---------------------------------------------------------------------------------------------------------
