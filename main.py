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

from decouple import config
import logging
import os
from datetime import datetime
import traceback

from setup.load_setup import load_setup
from matcher.setup import configs_correct, get_access_variables
from matcher.updater import update_cache
from matcher.match import match_strings, parse_source_file
from configs.config_checker import get_user_configs
from matcher.setup import create_configs_missing_file

__ENVDATA__ = config
load_setup(__ENVDATA__("CHECK_FOLDERS"),
           __ENVDATA__("LOAD_LOGGERS"))

__logger = logging.getLogger("main")
create_configs_missing_file()

# ---------------------------------------------------------------------------------------------------------
def load_debug_vars():
    test_excel_name = os.path.join(os.getcwd(), "TestSheet1.xlsx")

    return test_excel_name
# ---------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------
def run_matcher(dst_org="tecex--ruleseng", excel_name=None):
    debug_mode = 'true' in __ENVDATA__("DEBUG_MODE").lower()
    
    # --------- P0 --------------------------------------------------
    if debug_mode and 'true' in __ENVDATA__("load_test_file").lower():
        print("\t\n< Starting in DEBUG MODE >\n")
        excel_name = load_debug_vars()
    
    # # --------- P1 --------------------------------------------------
    # __logger.info("Checking configs ...") 
    # if not configs_correct():
    #     return 1
    
    # --------- P2 --------------------------------------------------
    __logger.info("Getting config data ...") 
    try:
        user_config = get_user_configs(dst_org)
        user_config = get_access_variables(user_config, __ENVDATA__)
    except Exception as e:
        __logger.info("Unable to read user configs from configs/user.ini")
        __logger.debug(e)
        return 2
    
    # --------- P3 --------------------------------------------------
    __logger.info("Checking folder structures ...") 
    path = os.path.join(os.getcwd(), 'cache', f"{user_config['dst_env']}")
    if not os.path.exists(path):
        os.mkdir(path)
    if not user_config['src_env'].lower() == 'excel':
        path = os.path.join(os.getcwd(), 'cache', f"{user_config['src_env']}")
        if not os.path.exists(path):
            os.mkdir(path)

    # --------- P4 --------------------------------------------------
    __logger.info("Accessing & Parsing data ... ") 
    if not user_config['src_details']:
        __logger.info("Parsing source file ")
        src_file, src_additional_info = parse_source_file(excel_name)

    # --------- P5 --------------------------------------------------
    __logger.info("Searching for matches ... \n")
    response = match_strings(src_file, 
                src_additional_info, 
                user_config=user_config, 
                env_vars=__ENVDATA__, 
                debug_mode=debug_mode)

# ---------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------
def main():
    start_time = datetime.now()

    try:
        run_matcher()
    except Exception as e:
        print("\nERROR DURING PROCESS! Please check the logs. \n")
        __logger.debug(f"{e} \n{traceback.format_exc()}")
    
    # --------- END -------------------------------------------------
    end_time = datetime.now()
    __logger.info(f"Process is complete. Total Time: {end_time-start_time}")

    return 0
# ---------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    print("------ RUNNING FROM main.py ------")

    main()
        # __logger.info(f"Error during process:\n{e}")
