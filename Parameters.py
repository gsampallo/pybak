import sys
import json,io
import os.path

class Parameters:

    def __init__(self):
        self.__file_config = "configuration.json"
        if not os.path.isfile(self.__file_config):
            print("There is not configuration file")
            sys.exit(1)
        else:
            self.load_parameters()

    def load_parameters(self):
        with open(self.__file_config) as json_file:
            data = json.load(json_file)
            self.database = data["database"]
            self.remote_path = data["remote_path"]
            self.local_path = data["local_path"]