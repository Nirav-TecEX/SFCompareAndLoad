"""
The user inputs a org either from the ini or an input, and this selects
which user credentials to use. The chosen user credentials 'selects' the
org to query and UPDATE from. 

For now all of the data comes from an excel spreadsheet. The user defines 
which org to try and find a matching string from. 

If DEBUG_MODE is True:
    1) main.py                  default test_sheet is loaded
    2) matcher/match.py         default id loaded
    3) matcher/updater.py       uses different time to check for updates 
"""

from decouple import config, AutoConfig
import logging
import os
from datetime import datetime
import traceback

from setup.load_setup import load_setup
from matcher.setup import configs_correct, get_access_variables
from matcher.match import match_strings, parse_source_file
from configs.config_checker import get_user_configs
from matcher.setup import create_configs_missing_file
from configs.config_checker import sf_Module_path

# __ENVDATA__ = config

__ENVDATA__ = AutoConfig(search_path=os.path.join(os.getcwd(), ".env"))
load_setup(__ENVDATA__("CHECK_FOLDERS"),
           __ENVDATA__("LOAD_LOGGERS"))

__logger = logging.getLogger("main_matcher")
create_configs_missing_file()

# ---------------------------------------------------------------------------------------------------------
def load_debug_vars():
    test_excel_name = os.path.join(sf_Module_path(), "Test_TestCases.xlsx")
    return test_excel_name
# ---------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------
def run_matcher(dst_org, excel_name):
    debug_mode = 'true' in __ENVDATA__("DEBUG_MODE").lower()
    
    # --------- P0 --------------------------------------------------
    if debug_mode and 'true' in __ENVDATA__("load_test_file").lower():
        print("\t\n< Starting in DEBUG MODE >\n")
        excel_name = load_debug_vars()
    
    # --------- P1 --------------------------------------------------
    __logger.info("Getting config data ...") 
    try:
        user_config = get_user_configs(dst_org)
        user_config = get_access_variables(user_config, __ENVDATA__)
    except Exception as e:
        __logger.info("Unable to read user configs from configs/user.ini")
        __logger.debug(e)
        return 2
    
    # --------- P2 --------------------------------------------------
    __logger.info("Checking folder structures ...") 
    path = os.path.join(sf_Module_path(), 'cache', f"{user_config['dst_env']}")
    if not os.path.exists(path):
        os.mkdir(path)
    if not user_config['src_env'].lower() == 'excel':
        path = os.path.join(sf_Module_path(), 'cache', f"{user_config['src_env']}")
        if not os.path.exists(path):
            os.mkdir(path)

    # --------- P3 --------------------------------------------------
    __logger.info("Accessing & Parsing data ... ") 
    if not user_config['src_details']:
        __logger.info("Parsing source file ")
        src_file, src_additional_info = parse_source_file(excel_name)

    # --------- P4 --------------------------------------------------
    __logger.info("Running match process")
    output_excel_name = excel_name.split(".xlsx")[0]+"-out"+".xlsx"
    __logger.info(f"Will write to {output_excel_name}")
    response = match_strings(src_file, 
                src_additional_info, 
                user_config=user_config, 
                env_vars=__ENVDATA__, 
                debug_mode=debug_mode,
                output_excel_name=output_excel_name)
    
    return output_excel_name

# ---------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------
def main(dst_org="tecex--ruleseng", excel_name=None):
    start_time = datetime.now()

    try:
        output_excel_name = run_matcher(dst_org, excel_name)
    except Exception as e:
        print("\nERROR DURING PROCESS! Please check the logs. \n")
        __logger.debug(f"{e} \n{traceback.format_exc()}")
        output_excel_name = None
    
    # --------- END -------------------------------------------------
    end_time = datetime.now()
    __logger.info(f"Process is complete. Total Time: {end_time-start_time}")

    return output_excel_name
# ---------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    print("------ RUNNING FROM main.py ------")

    _ = main()
