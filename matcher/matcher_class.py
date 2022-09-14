import logging
import json
import os

class Matcher:
    def __init__(self, src_file, src_additional_info):
        self.logger = logging.getLogger("matcher").getChild("MatcherClass")
        self.src_file = src_file
        self.src_additional_info = src_additional_info
        self.__src_id_obj_mappings = {}
        self.__loaded_dst_objs = {}
        self.__loaded_src_objs = {}
        
    @property
    def id_obj_mappings(self):
        return self.__src_id_obj_mappings

    @property
    def loaded_dst_objs(self):
        return self.__loaded_dst_objs

    @property
    def loaded_src_objs(self):
        return self.__loaded_src_objs

    def update_mappers(self, group_org_name, mappings_folder):
        if not self.mapping_loaded(group_org_name):
            self.logger.info(f"Getting mappings for {group_org_name}")
            id_obj_mappings_path = os.path.join(os.getcwd(), mappings_folder, f"{group_org_name}_mappings.json")
            self.id_obj_mappings[group_org_name] = self.load_src_id_obj_mappings(id_obj_mappings_path)
        else:
            self.logger.debug(f"Already have mappings for {group_org_name}")

    def mapping_loaded(self, org_name):
        return org_name in self.id_obj_mappings.keys()

    def load_src_id_obj_mappings(self, path):
        with open(path, 'r') as stream:
            mappings = json.load(stream)
        self.logger.debug(f"Mappings loaded from {path}")
        return mappings

    def search_for_object(self, id, org_name):
        # use the id (1st 3 letters) & org_name to get id
        pass

    def check_loaded_orgs_and_objects(self, group_org_name, object_name, type):
        is_loaded = {'org': False, 'object': False}
        obj_to_check = eval(f"self.loaded_{type}_objs")
        is_loaded['org'] = group_org_name in obj_to_check.keys() 

        try:
            is_loaded['object'] = object_name in obj_to_check[group_org_name].keys()
        except KeyError as e:
            self.logger.debug(f"Group org '{group_org_name}' and obj '{object_name}' not present.")
            is_loaded['object'] = False
  
    def update_data(self, type: str, data: dict):
        for key in data.keys():
            self.logger.debug(f"Updating {key} for {type}")
            if type == 'dst':
                self.__loaded_dst_objs[key] = data[key]
            elif type == 'src':
                self.loaded_src_objs[key] = data[key]
    
    def get_dst_id(self, id, object_name, src_org, dst_org):
        # use the object_name, src_org, dst_org to filter the loaded data
        # use the id to get matching string from src_objs then use that 
        # to match to dst_org and get dst_id.
        pass

    
