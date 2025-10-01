import yaml

class ConfigReader:
    config_data = {} #this is a diction {"key":"value"}
    def __init__(self, filename):
        self.filename = filename

    def readYML(self):
        with open(self.filename) as stream:
            try:
                self.config_data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
    
    def printConfigData(self):
        for key, value in self.config_data.items():
            print(f"{key}: {value}")

    def get(self, key):
        return self.config_data.get(key)