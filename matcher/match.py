import logging
import os
import pandas as pd

from .setup import create_query_strs
from .salesforce import ComplexSF

__logger = logging.getLogger("matcher").getChild(__name__)

# # ---------------------------------------------------------------------------------------------------------
# def update_cache(user_config, dict_of_query_strs=None):
#     """ This function should check the necessary destination and source orgs and update the required 
#         files as needed. It will update if the last update was not performed within the last 7 days. 

#         param :: user_config          takes the data read from the user_config to know which orgs to check 
#                                       for recently updated time.
        
#         (DEPRECATED) 
#         param :: dict_of_query_strs   takes a dict of the generated query strs which were generated from 
#                                       the user configs.
        
#         Still need to implement the timer checker. """

#     __logger.info(f"Creating queries for updates ")
#     dict_of_query_strs = create_query_strs(user_config['obj_list'])
#     print("Queries:")
#     for key in dict_of_query_strs:
#         print(f"\t {dict_of_query_strs[key]}")

#     sf = ComplexSF(user_config['dst_env'],
#                    user_config['details']['username'],
#                    user_config['details']['password'],
#                    user_config['details']['token']) # sandbox=user_config['dst_env']

#     for obj_key in dict_of_query_strs:
#         records = sf.perform_query(dict_of_query_strs[obj_key])
#         records_with_match_str = create_match_string(records, obj_key)

#         save_records(records_with_match_str,
#                         obj_key, 
#                         user_config['dst_env'],
#                         sf)
# # ---------------------------------------------------------------------------------------------------------

# # ---------------------------------------------------------------------------------------------------------
# def create_match_string(records, obj_key):
#     records_with_match_str = []
#     for record in records:
#         match_str = ''
#         for attribute in record.keys():
#             if attribute != 'attributes' and attribute != 'Id':
#                 if record[attribute]:
#                     attr_str = record[attribute]
#                 else:
#                     attr_str = ''
#                 match_str = match_str + f"[{attr_str}]"
#         match_str = match_str + f"@{obj_key}"
#         record["Matching String"] = match_str
#         records_with_match_str.append(record)
#     return records_with_match_str
# # ---------------------------------------------------------------------------------------------------------

# # ---------------------------------------------------------------------------------------------------------
# def save_records(records, obj, dst_env, sfObj: ComplexSF):
#     path = os.path.join(os.getcwd(), 'cache', f'{dst_env}')
#     if isinstance(sfObj.environment, str):
#         excel_path = os.path.join(path, f"{obj}-{sfObj.environment}.xlsx")
#     else:
#         excel_path = os.path.join(path, f"{obj}.xlsx")
#     with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
#         df = pd.DataFrame.from_dict(records)
#         df.to_excel(writer)
# # ---------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------
def match_ids(obj, src_org, dst_org, id=None):
    match_strings(obj, src_org, dst_org, id)
# ---------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------
def match_strings(src_exl, dst_org='tecex--prod', obj=None, id=None):
    """ Takes id(s) and maps it from its current org to another org. The current state of org ids are 
        loaded from the current excel files in the cache/ORG_NAME folder. 

        FOR THE SOURCE: The obj name, ids and src_org are read from the excel file

        param   :: src_exl      path to the excel for the source data
        param   :: dst_org      the dst_org for the ids
        param   :: obj          the object whose ids should be matched between orgs. Usually read from
                                the excel.

        Required Sheet Layout
         _______________________________
        | Add Info 1 | Details 1 ...   |
        | Add Info 2 | Details 2 ...   |
        | Add Info 3 | Details 3 ...   |
        ...
        ... 
         _____________________________________________________________________________
        | Input Keys | Input Key Value | Mod | Output Key | Output Key Value | Notes |
        
        Imporvements:
        - First implementation: Reads 1 sheet, for data. Dummy orgs in a Dummy excel.  
        - Currently only reads 1 sheet- should cycle through
        - Can pssibly be made faster with searching algorithms. 
        
    """
    
    src_excel_path = os.path.join(os.getcwd(), f"{src_exl}")
    src_excel = excelWB_to_dict(src_excel_path)
    src_excel_rewrite = {}

    # runs over each sheet
    for sheet in src_excel.keys():
        src_org = get_additional_information("salesforceorg", src_excel[sheet])

    dst_org_excel_path = os.path.join(os.getcwd(), 'cache', dst_org, f"{obj}.xlsx")
    dst_org_excel = pd.read_excel(dst_org_excel_path)

    src_org_excel_path = os.path.join(os.getcwd(), 'cache', src_org, f"{obj}.xlsx")
    src_org_excel = pd.read_excel(src_org_excel_path)




    pass
# ---------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------
def excelWB_to_dict(excel_file_path):
        files = pd.ExcelFile(excel_file_path)
        data = {}
        for sheet_name in files.sheet_names:
            sheet = pd.read_excel(files, sheet_name=sheet_name)
            data[sheet_name] = sheet
        
        return data
# ---------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------
def get_additional_information(add_info_key, df, max_num_of_add_fields=100):
    """ This function goes through the beginning of the excel, and its COLUMN 1, and searches for the 
        'add_info_key' variable provided. 

        param :: add_info_key   indicates which additional information to get. 
                                Selects the data in the same row, but next column.  
                                
        Returns None if the the row with key 'Input Keys' is reached, or if the number of addtional fields
        is greater than max_num_of_add_fields.                         
    """
    
    end_of_add_info_key = 'Input Keys'
    for row in range(0, max_num_of_add_fields):
        if df.iloc[row,0].replace(" ", "").lower() == add_info_key:
            return df.iloc[row,1]
        elif df.iloc[row,0] == end_of_add_info_key:
            return None
    return None
# ---------------------------------------------------------------------------------------------------------
