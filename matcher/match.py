import os
import pandas as pd

from .salesforce import ComplexSF

# ---------------------------------------------------------------------------
def update_cache(user_config, dict_of_query_strs):
    """ This function should check the necessary destination and source
        orgs and updates the required files as needed. It will update if 
        the last update was not performed within the last 7 days. 
        
        Still need to implement the timer checker. """

    sf = ComplexSF(user_config['dst_env'],
                   user_config['details']['username'],
                   user_config['details']['password'],
                   user_config['details']['token']) # sandbox=user_config['dst_env']

    for obj_key in dict_of_query_strs:
        records = sf.perform_query(obj_key, 
                                   dict_of_query_strs[obj_key], 
                                   user_config['dst_env'])
        records_with_match_str = create_match_string(records, obj_key)

        save_records(records_with_match_str,
                        obj_key, 
                        user_config['dst_env'],
                        sf)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
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
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
def save_records(records, obj, dst_env, sfObj: ComplexSF):
    path = os.path.join(os.getcwd(), 'cache', f'{dst_env}')
    if isinstance(sfObj.environment, str):
        excel_path = os.path.join(path, f"{obj}-{sfObj.environment}.xlsx")
    else:
        excel_path = os.path.join(path, f"{obj}.xlsx")
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        df = pd.DataFrame.from_dict(records)
        df.to_excel(writer)
# ---------------------------------------------------------------------------
