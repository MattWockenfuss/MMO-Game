import yaml
import os

class ConfigManager():
    def __init__(self):
        self.database = {
                            "tiles": [],
                            "recipes": [],
                            "enemies": [],
                            "items": [],
                            "players": [],
                            "worlds": []
                        }

    def readDirectory(self, path, atRoot = True):
        if atRoot:
            self.database = {
                    "tiles": [],
                    "recipes": [],
                    "enemies": [],
                    "items": [],
                    "players": [],
                    "worlds": []
                }
            print(self.database)
        print(f"Reading {path}")
        names = os.listdir(path)
        for name in names:
            fullpath = os.path.join(path, name)
            
            if os.path.isdir(fullpath):
                self.readDirectory(fullpath, False)
            else:
                filename, extension = os.path.splitext(name)
                match extension:
                    case ".png":
                        continue
                    case ".yml":
                        data = self.readYML(fullpath)
                        pieces = path.replace("\\", "/").split("/")
                        match pieces[1]:
                            case "assets":
                                self.database["tiles"].append(data)
                            case "enemies":
                                self.database["enemies"].append(data)
                            case "items":
                                self.database["items"].append(data)
                            case "players":
                                self.database["players"].append(data)
                            case "recipes":
                                self.database["recipes"].append(data)
                            case "worlds":
                                self.database["worlds"].append(data)
        if(atRoot):
            #alright when we are done, print out the number of files loaded!
            total = 0
            for key, value in self.database.items():
                #print(f"{key} {len(value)}")
                total += len(value)

            print(f"Loaded {total} YML Files!")


    def readYML(self, path):
        #print("[READING YML]", path)
        with open(path) as stream:
            try:
                data = yaml.safe_load(stream)
                return data 
            except yaml.YAMLError as exc:
                print(exc)
    

    def printDirectories(self, path, indentLevel):
        names = os.listdir(path)
        for name in names:
            fullpath = os.path.join(path, name)
            print(f"|", end="")
            if os.path.isdir(fullpath):    #its a direcory
                print("---" * indentLevel, f"{name}/")
                self.printDirectories(fullpath, indentLevel + 1)
            else:                           #its a file
                filename, extension = os.path.splitext(name)
                print("    " * indentLevel, f"{filename}{extension}")



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