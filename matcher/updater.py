import logging
import os
import pandas as pd

from .setup import create_query_strs
from .salesforce import ComplexSF

__logger = logging.getLogger("matcher").getChild(__name__)

# ---------------------------------------------------------------------------------------------------------
def update_cache(user_config, dict_of_query_strs=None):
    """ This function should check the necessary destination and source orgs and update the required 
        files as needed. It will update if the last update was not performed within the last 7 days. 

        param :: user_config          takes the data read from the user_config to know which orgs to check 
                                      for recently updated time.
        
        (DEPRECATED) 
        param :: dict_of_query_strs   takes a dict of the generated query strs which were generated from 
                                      the user configs.
        
        Still need to implement the timer checker. """

    __logger.info(f"Creating queries for updates ")
    dict_of_query_strs = create_query_strs(user_config['obj_list'])
    __logger.debug("Queries:")
    for key in dict_of_query_strs:
        __logger.debug(f"\t {dict_of_query_strs[key]}")

    __logger.info(f"Updating excels in ../cache/.. ")
    sf = ComplexSF(user_config['dst_env'],
                   user_config['details']['username'],
                   user_config['details']['password'],
                   user_config['details']['token']) # sandbox=user_config['dst_env']

    for obj_key in dict_of_query_strs:
        records = sf.perform_query(dict_of_query_strs[obj_key])
        __logger.debug(f"Creating match string for {obj_key}")
        records_with_match_str = create_match_string(records, obj_key)

        save_records(records_with_match_str,
                        obj_key, 
                        user_config['dst_env'],
                        sf)
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
    path = os.path.join(os.getcwd(), 'cache', f'{dst_env}')
    if isinstance(sfObj.environment, str):
        excel_path = os.path.join(path, f"{obj}-{sfObj.environment}.xlsx")
    else:
        excel_path = os.path.join(path, f"{obj}.xlsx")
    __logger.debug(f"Saving to: {excel_path} ")
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        df = pd.DataFrame.from_dict(records)
        df.to_excel(writer)
# ---------------------------------------------------------------------------------------------------------
