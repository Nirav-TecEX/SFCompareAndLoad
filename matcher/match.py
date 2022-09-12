import logging
import os
import pandas as pd

from .salesforce import ComplexSF

__logger = logging.getLogger("matcher").getChild(__name__)

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

    src_file, additional_information = parse_source_file(os.path.join(os.getcwd(), f"{src_exl}"))

    dst_org_excel_path = os.path.join(os.getcwd(), 'cache', dst_org, f"{obj}.xlsx")
    dst_org_excel = pd.read_excel(dst_org_excel_path)

    src_org_excel_path = os.path.join(os.getcwd(), 'cache', src_org, f"{obj}.xlsx")
    src_org_excel = pd.read_excel(src_org_excel_path)




    pass
# ---------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------
def parse_source_file(path):
    """ Takes the source excel and loads it into a json format in a dict. 
    
        Returns the json-dict source excel and a dict of additional information for each sheet. The
        additional information is also saved with its location (row, column).

        Additional information: org, input_key_start.    
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
def is_id(value):
    """ Checks if the value can possibly be a SalesForce id. Returns a bool. 
    """
    pass

# ---------------------------------------------------------------------------------------------------------
