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
        updates with. """
    access_str = ''
    
    dest_org = user_config['dst_env']
    org = dest_org.split('--')[1]
    if 'tec' in dest_org:
        access_str = access_str + 'tec_'
    elif 'zee' in dest_org:
        access_str = access_str + 'zee_'
    elif 'med' in dest_org:
        access_str = access_str + 'med_' 

    if not 'prod' in org:
        access_str = access_str + org + "_"
    # if_stage = ''
    # env = user_config['org_env']
    # if not 'prod' in env:
    #     access_str = access_str + 'Stage'
    #     if_stage = '_'
    
    user_config['details'] = \
    {'username': __envdata__(f'{access_str}Username'),
     'password': __envdata__(f'{access_str}Password'),
     'token': __envdata__(f'{access_str}Token')}

    return user_config
    
# ---------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------
def create_query_strs(obj_list):
    dict_of_query_strs = {}
    for obj_name in obj_list:       
        obj_list[obj_name]['min_fields'].insert(0, 'Id')
        selections = ', '.join(obj_list[obj_name]['min_fields'])
        query_str = f"SELECT {selections} FROM {obj_name}"
        dict_of_query_strs[obj_name] = query_str
        
    return dict_of_query_strs
# ---------------------------------------------------------------------------------------------------------
