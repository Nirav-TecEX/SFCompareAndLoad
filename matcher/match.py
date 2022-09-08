from .salesforce import ComplexSF

def update_dest_cache(user_config, dict_of_query_strs): 
    update_cache(user_config, dict_of_query_strs)

def update_cache(user_config, dict_of_query_strs):
    sf = ComplexSF(user_config['org_env'],
                   user_config['details']['username'],
                   user_config['details']['password'],
                   user_config['details']['token']) # sandbox=user_config['dst_env']
    for key in dict_of_query_strs:
        records = sf.perform_query(key, dict_of_query_strs[key], 
                                   user_config['dst_env'])