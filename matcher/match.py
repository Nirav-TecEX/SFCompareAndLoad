import logging
import os
import pandas as pd
import json

from .salesforce import ComplexSF
from .matcher_class import Matcher

__logger = logging.getLogger("matcher").getChild(__name__)

# ---------------------------------------------------------------------------------------------------------
def load_match_string_debug_vars():
    pass
# ---------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------
def match_strings(src_file, src_additional_info, dst_org='tecex--prod', obj=None, id=None, env_vars=None, debug_mode=False):
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

    mappings_folder = os.path.join(os.getcwd(), env_vars("id_org_mapper_relative_path").replace("/", os.sep))
    dst_path = os.path.join(os.getcwd(), "cache", f"{dst_org}")
    __logger.info(f"Using destination data from: {dst_path}")
    
    matching_obj = Matcher(src_file, src_additional_info)
    
    for sheet in matching_obj.src_file.keys():
        src_org = matching_obj.src_additional_info[sheet]['org'][0]
        input_key_row = src_additional_info[sheet]['input_key_start'][1][0]
        # new_sheet = src_file[sheet][input_key_row_col[0]:]
        # new_sheet.columns = new_sheet.iloc[0]
        new_sheet = src_file[sheet]
        group_org_name = src_org.split("--")[0]
        matching_obj.update_mappers(group_org_name, mappings_folder)
        # at this point, i have the mapper for the group org- like tecex, zee or medical
        # which will allow me to take an id and match it to its object type
        # I would now go through each id in the excel and:
        #   1) see which object type it is
        #   2) go to the SRC ORG and load the OBJ datasheet (load in the class)
        #          -> if it is not present
        #   3) use the id to get the objs matching string
        #   4) go to the DST ORG and load the OBJ datasheet (load in the class)
        #          -> if it is not present
        #   5) use the matching string to find it corresponding id
        #   6) update excel dict
        #   7) write to new excel 



        # --- Done for each id in sheet ---
        # for row in 
        for row_index in range(input_key_row, len(new_sheet)):
            id = new_sheet.iloc[row_index, 1]
            new_id = id

            if is_id(id):
                # 1
                if debug_mode:
                    object_name = 'CPA_v2_0__c'
                    id = "a26070000008Qy1AAE"
                else:
                    object_name = matching_obj.get_object_type(id, group_org_name)

                # checking if the datasheets for the objects from the source and desitnation orgs are loaded
            
                matching_obj.check_loaded_orgs_and_objects(dst_org, object_name)
                matching_obj.check_loaded_orgs_and_objects(src_org, object_name, type='src')

                obj_matching_string = matching_obj.get_src_match_string(id, src_org, object_name)
                
                if isinstance(obj_matching_string, int):
                    continue
                
                new_id = matching_obj.match_id_to_dst_org(obj_matching_string, dst_org, object_name)
                if debug_mode:
                    new_id = "UPDATED - " + new_id
            
            new_sheet.iloc[row_index, 1] = new_id
        
        src_file[sheet] = new_sheet 

    # run src_file["Sheet1"][98:99]   
    if debug_mode:
        __logger.info(f"New Id: {src_file['Sheet1'][98:99]}")
        __logger.info(f"New Id: {src_file['Sheet2'][98:99]}")
    write_to_output_excel(src_file)

    return 0

# ---------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------
def parse_source_file(path):
    """ Takes the source excel and loads it into a json format in a dict. 
    
        Returns the json-dict source excel and a dict of additional information for each sheet. The
        additional information is also saved with its location (row, column).

        Additional information: org, input_key_start.  

        *** See function 'match_strings' for explanation on required excel layout.  
    """

    src_excel = excelWB_to_dict(path)
    src_excel_rewrite = {}

    additional_information = {}
    add_info_map_to_excel_key = {'org': "salesforceorg",
                                 'input_key_start': "inputkeys"} 
    for sheet in src_excel.keys():
        additional_information[sheet] = {}
        for add_info_item in add_info_map_to_excel_key.keys():
            additional_information[sheet][add_info_item] = \
            get_additional_information(add_info_map_to_excel_key[add_info_item], src_excel[sheet])

    return src_excel, additional_information
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

        Returns a tuple of its value and location in the form: (value, (row, column)).

        Returns None if the the row with key 'Input Keys' is reached, or if the number of addtional fields
        is greater than max_num_of_add_fields.         

        Can possibly be made faster using pandas filters.                
    """
    
    end_of_add_info_key = 'Input Keys'
    for row in range(0, max_num_of_add_fields):
        try:
            if df.iloc[row,0].replace(" ", "").lower() == add_info_key:
                return (df.iloc[row,1], (row,1))
            elif df.iloc[row,0] == end_of_add_info_key:
                return None
        except AttributeError as e:
            # accounts for nan
            pass

    return None
# ---------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------
def is_id(id):
    """ Checks if the value can possibly be a SalesForce id. Returns a bool. 
    """
    try:
        if (len(id) == 18) and (not ' ' in id):
            return True
    except Exception as e:
        pass
    return False
# ---------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------
def write_to_output_excel(src_file):
    """ Creates an output file with the new data. """
    pass
# ---------------------------------------------------------------------------------------------------------

