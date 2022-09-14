"""
The user inputs a org either from the ini or an input, and this selects
which user credentials to use. The chosen user credentials 'selects' the
org to query and UPDATE from. 

For now all of the data comes from an excel spreadsheet. The user defines 
which org to try and find a matching string from. 
"""

from decouple import config
import logging
import os
from datetime import datetime

from setup.load_setup import load_setup
from matcher.setup import configs_correct, get_access_variables
from matcher.updater import update_cache
from matcher.match import match_ids, match_strings, parse_source_file
from configs.config_checker import get_user_configs

__ENVDATA__ = config
load_setup(__ENVDATA__("CHECK_FOLDERS"),
           __ENVDATA__("LOAD_LOGGERS"))

__logger = logging.getLogger("main")

# ---------------------------------------------------------------------------------------------------------
def load_debug_vars():
    test_excel_name = os.path.join(os.getcwd(), "TestSheet1.xlsx")

    return test_excel_name
# ---------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------
def main(excel_name=None):
    start_time = datetime.now()

    if 'true' in __ENVDATA__("DEBUG_MODE").lower():
        print("\t\n< Starting in DEBUG MODE >\n")
        excel_name = load_debug_vars()
    
    # --------- P1 --------------------------------------------------
    if not configs_correct():
        return 1
    
    # --------- P2 --------------------------------------------------
    try:
        user_config = get_user_configs()
        user_config = get_access_variables(user_config, __ENVDATA__)
    except Exception as e:
        __logger.info("Unable to read user configs from configs/user.ini")
        __logger.debug(e)
        return 2
    
    # --------- P4 --------------------------------------------------
    __logger.info("Checking folder structures ...") 
    path = os.path.join(os.getcwd(), 'cache', f"{user_config['dst_env']}")
    if not os.path.exists(path):
        os.mkdir(path)
    if not user_config['src_env'].lower() == 'excel':
        path = os.path.join(os.getcwd(), 'cache', f"{user_config['src_env']}")
        if not os.path.exists(path):
            os.mkdir(path)

    # --------- P5 --------------------------------------------------
    # creates the query str and then updates cache.    
    # this update cache uses data from the user.ini and updates for all necessary orgs and objects. 
    # Can add a check time last updated to prevent always updating 
    __logger.info("Updating caches ... ") 
    update_cache('dst', user_config, dict_of_query_strs=None, env_vars=__ENVDATA__)
    update_cache('src', user_config, dict_of_query_strs=None, env_vars=__ENVDATA__)

    # --------- P6 --------------------------------------------------
    __logger.info("Accessing & Parsing data ... ") 
    if not user_config['src_details']:
        __logger.info("Parsing source file ")
        src_file, src_additional_info = parse_source_file(excel_name)

    # --------- P7 --------------------------------------------------
    __logger.info("Searching for matches ... ") 
    match_strings(src_file, src_additional_info, env_vars=__ENVDATA__)

    # --------- END -------------------------------------------------
    end_time = datetime.now()
    __logger.info(f"Process is complete. Total Time: {end_time-start_time}")
# ---------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    print("------ RUNNING FROM main.py ------")

    try:
        main()
    except Exception as e:
        __logger.debug(f"Error during process:\n{e}")
