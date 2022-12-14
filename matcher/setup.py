import logging
from configs.config_checker import check_configs_exist 

__setup_logger = logging.getLogger("main").getChild(__name__)

# ---------------------------------------------------------------------------------------------------------
def configs_correct():

    print("Checking configs")
    some_configs_not_present = check_configs_exist()

    if some_configs_not_present:
        print("--- CONFIGS NOT PRESENT ---")
        for config_not_present in some_configs_not_present:
            print(f"\t {config_not_present}") 
        print("Please update files and try again.")
        return False
    else:
        __setup_logger.info("All config files present. ")
        return True
# ---------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------
def get_access_variables(user_config, __envdata__):
    """ Creates the user's config and the selects which user to perform
        updates with. 
    """

    user_config = get_details('dst_env', user_config, __envdata__)
    user_config = get_details('src_env', user_config, __envdata__)        

    return user_config
    
# ---------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------
def get_details(org_env, user_config, __envdata__):
    """ Attempts to get the details for the org_env defined. Usually used to get the details for the 
        destination and source orgs. 
    """
    org_type = org_env.split("_")[0]
    access_str = ''
    dest_org = user_config[org_env]
    if dest_org == 'excel':
        user_config[f'{org_type}_details'] = None
        return user_config
    org = dest_org.split('--')[1]
    
    if 'tec' in dest_org:
        access_str = access_str + 'tec_'
    elif 'zee' in dest_org:
        access_str = access_str + 'zee_'
    elif 'med' in dest_org:
        access_str = access_str + 'med_' 

    if not 'prod' in org:
        access_str = access_str + org + "_"
    
    user_config[f'{org_type}_details'] = \
    {'username': __envdata__(f'{access_str}Username'),
     'password': __envdata__(f'{access_str}Password'),
     'token': __envdata__(f'{access_str}Token')}

    return user_config
# ---------------------------------------------------------------------------------------------------------
