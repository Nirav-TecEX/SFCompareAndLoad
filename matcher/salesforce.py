"""
Module to make accessing, adding and changing data on salesforce easier.
"""

import simple_salesforce as sf
import os
import pandas as pd

class ComplexSF(sf.Salesforce):
    def __init__(self, environment, username, password, token, sandbox=None):
        self.environment = 'production' if 'prod' in environment.lower() else 'staging'
        self.__username = username
        self.__password = password
        self.__token = token
        # self.__domain = user_config['dst_env']
        self.__domain = sandbox

        super().__init__(username=self.__username,
                         password=self.__password,
                         security_token=self.__token,
                         domain=self.__domain)

    def perform_query(self, obj, query_str, dst_env):
        response = self.query_all(query_str)
        if response['totalSize'] < 1:
            print(f"No records that match query: {query_str}")
            return None
        else:
            print("Saving list of of records. ")
            records = response['records']
            sorted_records = sorted(records, key=lambda record: record['Id'])
            path = os.path.join(os.getcwd(), 'cache', f'{dst_env}')
            if not os.path.exists(path):
                os.mkdir(path)
            excel_path = os.path.join(path, f"{obj}.xlsx")
            with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                df = pd.DataFrame.from_dict(sorted_records)
                df.to_excel(writer)
            return response['records']

    def perform_reverse_query(self, obj, obj_id):
        pass

if __name__ == "__main__":
    print("Testing salesforce.py. ")
    print("----------------------------------")
    print("               PROD")
    print("----------------------------------")
    test = ComplexSF("production")
    print("----------------------------------")
    print("              STAGE")
    print("----------------------------------")
    test = ComplexSF("staging")
    print("----------- END ------------")