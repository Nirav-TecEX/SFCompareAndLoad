from decouple import config
import logging

from setup.load_setup import load_setup
from matcher.setup import configs_correct, get_access_variables, create_query_strs
from matcher.match import update_cache
from configs.config_checker import get_user_configs

__ENVDATA__ = config
load_setup(__ENVDATA__("CHECK_FOLDERS"),
           __ENVDATA__("LOAD_LOGGERS"))

__logger = logging.getLogger("main")

#----------------------------------------------------------------------------
def main():
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
    
    # --------- P3 --------------------------------------------------
    __logger.info(f"Running the match algorithm for: {', '.join(user_config['obj_list'])}")
    dict_of_query_strs = create_query_strs(user_config['obj_list'])
    print("Queries:")
    for key in dict_of_query_strs:
        print(f"\t {dict_of_query_strs[key]}")
    
    # --------- P4 --------------------------------------------------
    update_cache(user_config, dict_of_query_strs)

#----------------------------------------------------------------------------

if __name__ == "__main__":
    print("------ RUNNING FROM main.py ------")

    main()
