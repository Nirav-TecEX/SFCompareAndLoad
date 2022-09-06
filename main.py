from decouple import config
import logging

from setup.load_setup import load_setup
from configs.config_checker import check_configs_exist

__ENVDATA__ = config
load_setup(__ENVDATA__("CHECK_FOLDERS"),
           __ENVDATA__("LOAD_LOGGERS"))

def main():
    __logger = logging.getLogger("main")
    some_configs_not_present = check_configs_exist()

    if some_configs_not_present:
        print("--- CONFIGS NOT PRESENT ---")
        for config_not_present in some_configs_not_present:
            print(f"\t {config_not_present}") 
        print("Please update files and try again.")
        return 1
    else:
        __logger.info("All config files present. ")


if __name__ == "__main__":
    print("------ RUNNING FROM main.py ------")

    main()
