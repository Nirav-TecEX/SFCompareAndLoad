from decouple import config
from setup.load_setup import load_setup

__CONFIGDATA__ = config
load_setup(__CONFIGDATA__("CHECK_FOLDERS"),
           __CONFIGDATA__("LOAD_LOGGERS"))

if __name__ == "__main__":
    print("------ RUNNING FROM main.py ------")
