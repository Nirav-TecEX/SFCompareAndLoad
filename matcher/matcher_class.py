import logging
import json
import os
import pandas as pd

from matcher.updater import should_not_update_file, update_id_to_obj_mapper

class Matcher:
    def __init__(self, update_time, src_file, src_additional_info):
        self.logger = logging.getLogger("MatcherClass")
        self.update_time = int(update_time)
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

    def update_mappers(self, group_org_name, mappings_folder, sfObj=None):
        if not self.mapping_loaded(group_org_name):
            self.logger.debug(f"Loading mappings for {group_org_name}")
            id_obj_mappings_path = os.path.join(os.getcwd(), mappings_folder, f"{group_org_name}_mappings.json")
            if not should_not_update_file(id_obj_mappings_path, self.update_time):
                update_id_to_obj_mapper(id_obj_mappings_path, sfObj)
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

    def get_object_type(self, id, group_org_name):
        id_classifier = id[0:3]
        return self.id_obj_mappings[group_org_name][id_classifier]

    def check_loaded_orgs_and_objects(self, org_name, object_name, type='dst'):
        is_loaded = {'org': False, 'object': False}
        obj_to_check = eval(f"self.loaded_{type}_objs")
        is_loaded['org'] = org_name in obj_to_check.keys() 

        if is_loaded['org']:
            try:
                is_loaded['object'] = object_name in obj_to_check[org_name].keys()
            except KeyError as e:
                self.logger.debug(f"obj '{object_name}' not present.")
                is_loaded['object'] = False
        else:
            self.logger.debug(f"Group org '{org_name}' and obj '{object_name}' not present.")
            is_loaded['object'] = False

        if not is_loaded['org'] and not is_loaded['object']:
            self.logger.debug(f"Adding org and obj: {org_name} - {object_name}")
            obj_to_check[org_name] = {}
            obj_to_check[org_name] = self.__load_obj_data(org_name, object_name)
        elif not is_loaded['object']:
            self.logger(f"Adding obj to org: {object_name} - {org_name}")
            obj_to_check[org_name] = self.__load_obj_data(org_name, object_name)
        else:
            self.logger.info(f"Unable to check data for: {type} - {org_name} - {object_name}")

    def __load_obj_data(self, org_name, object_name):
        excel_path = os.path.join(os.getcwd(), "cache", org_name, f"{object_name}.xlsx")
        self.logger.debug(f"Loading object data from: {excel_path}")
        data = {}
        try:
            obj_excel_file = pd.ExcelFile(excel_path)
            sheet = pd.read_excel(obj_excel_file)
            data[object_name] = sheet
        except FileNotFoundError as e:
            pass
        return data
    
    def get_src_match_string(self, id, src_org, object_name):
        self.logger.info(f"Getting src match string for {id}: {src_org} - {object_name}")
        obj_data = self.loaded_src_objs[src_org][object_name]
        matching_string = obj_data[obj_data["Id"] == id]
        if len(matching_string) == 1:
            return matching_string.loc[matching_string.index[0], "Matching String"]
        else:
            return 1
    
    def match_id_to_dst_org(self, matching_string, dst_org, object_name):
        obj_data = self.loaded_dst_objs[dst_org][object_name]
        new_id = obj_data[obj_data["Matching String"] == matching_string]
        if len(new_id) == 1:
            return new_id.loc[new_id.index[0], "Id"]
        elif len(new_id) > 1:
            # add fields to matching string
            return 1
        else:
            return 2
    
    def update_data(self, type: str, data: dict):
        for key in data.keys():
            self.logger.debug(f"Updating {key} for {type}")
            if type == 'dst':
                self.__loaded_dst_objs[key] = data[key]
            elif type == 'src':
                self.loaded_src_objs[key] = data[key]    
