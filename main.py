from decouple import config
import logging

from setup.load_setup import load_setup
from configs.config_checker import check_configs_exist, get_user_configs

__ENVDATA__ = config
load_setup(__ENVDATA__("CHECK_FOLDERS"),
           __ENVDATA__("LOAD_LOGGERS"))

#----------------------------------------------------------------------------
def configs_correct():
    __logger = logging.getLogger("main")

    print("Checking configs")
    some_configs_not_present = check_configs_exist()

    if some_configs_not_present:
        print("--- CONFIGS NOT PRESENT ---")
        for config_not_present in some_configs_not_present:
            print(f"\t {config_not_present}") 
        print("Please update files and try again.")
        return False
    else:
        __logger.info("All config files present. ")
        return True
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
def get_access_variables(user_config):
    access_str = ''
    
    dest_org = user_config['dst_env']
    if 'tec' in dest_org:
        access_str = access_str + 'tec_'
    elif 'zee' in dest_org:
        access_str = access_str + 'zee_'
    elif 'med' in dest_org:
        access_str = access_str + 'med_' 
    
    if_stage = ''
    env = user_config['org_env']
    if not 'prod' in env:
        access_str = access_str + 'Stage'
        if_stage = '_'
    
    user_config['details'] = \
    {'username': __ENVDATA__(access_str.replace('_', f'_Username{if_stage}')),
     'password': __ENVDATA__(access_str.replace('_', f'_Password{if_stage}')),
     'token': __ENVDATA__(access_str.replace('_', f'_Token{if_stage}'))}

    return user_config
    
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
def main():
    __logger = logging.getLogger("main")

    if not configs_correct():
        return 1
    
    try:
        user_config = get_user_configs()
        user_config = get_access_variables(user_config)
    except Exception as e:
        __logger.info("Unable to read user configs from configs/user.ini")
        __logger.debug(e)
        return 2
    
    __logger.info(f"Running the match algorithm for: {', '.join(user_config['obj_list'])}")

#----------------------------------------------------------------------------

if __name__ == "__main__":
    print("------ RUNNING FROM main.py ------")

    main()
