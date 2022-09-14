import logging
import json
import os

class Matcher:
    def __init__(self):
        self.logger = logging.getLogger("matcher").getChild("MatcherClass")
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
            self.__src_id_obj_mappings[group_org_name] = self.load_src_id_obj_mappings(id_obj_mappings_path)
        else:
            self.logger.debug(f"Already have mappings for {group_org_name}")

    def mapping_loaded(self, org_name):
        return org_name in self.__src_id_obj_mappings.keys()

    def load_src_id_obj_mappings(self, path):
        with open(path, 'r') as stream:
            mappings = json.load(stream)
        self.logger.debug(f"Mappings loaded from {path}")
        return mappings

    def update_data(self, type: str, data: dict):
        for key in data.keys():
            self.logger.debug(f"Updating {key} for {type}")
            if type == 'dst':
                self.__loaded_dst_objs[key] = data[key]
            elif type == 'src':
                self.__loaded_src_objs[key] = data[key]

    
