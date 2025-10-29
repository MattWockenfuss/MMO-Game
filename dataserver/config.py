import yaml
import os
import utils

class ConfigManager():
    def __init__(self):
        self.database = {
                            "tiles": [],
                            "recipes": [],
                            "enemies": [],
                            "statics": [],
                            "items": [],
                            "players": [],
                            "tileMap": {},
                            "worlds": []
                        }
    #this is disgusting, fix later
    def readDirectory(self, path, atRoot = True):
        if atRoot:
            self.database = {
                    "tiles": [],
                    "recipes": [],
                    "enemies": [],
                    "statics": [],
                    "items": [],
                    "players": [],
                    "tileMap": {},
                    "worlds": []
                }
            print(self.database)
        print(f"Reading {path}")
        names = os.listdir(path)
        #print(names)
        for name in names:
            fullpath = os.path.join(path, name)
            
            if os.path.isdir(fullpath):
                self.readDirectory(fullpath, False)
            else:
                filename, extension = os.path.splitext(name)
                match extension:
                    case ".yml":
                        data = utils.readYML(fullpath)
                        *pieces, file_name = fullpath.replace("\\", "/").split("/")
                        print(f"{pieces} -> {file_name}")
                        match pieces[1]:
                            case "items":
                                self.database["items"].append(data)
                            case "players":
                                self.database["players"].append(data)
                            case "recipes":
                                self.database["recipes"].append(data)
                            case "worlds":
                                #okay so whatever this is, its in world folder, check to see if its in tile folder
                                #we also only want to read the worldname.yml
                                if pieces[2] == "_tiles":
                                    #then this is a tile
                                    self.database["tiles"].append(data)
                                if pieces[2] == "_static_entities":
                                    self.database["statics"].append(data)
                                else:
                                    if filename == pieces[2]:
                                        data["folderName"] = pieces[2]
                                        self.database["worlds"].append(data)
                                    else:
                                        pass
                                        #print(f"SKIPPING {filename} in {path}")

        if(atRoot):
            #alright when we are done, print out the number of files loaded!
            total = 0
            for key, value in self.database.items():
                #print(f"{key} {len(value)}")
                total += len(value)

            print(f"Loaded {total} YML Files!")

            self.database["tileMap"] = utils.generateTileMappings(self.database)

            for worldDict in self.database["worlds"]:
                print()
                print(f"-------- {worldDict.get("World-Name")} --------")
                #okay so we need a mapping of code names to IDs, global or world based?
                #okay so every world can have a mappings file mapping color to code name to ID?
                #or every tile has a set color, and the data server dynamically generates IDs on startup.
                #then it sends these to all the worlds and eventually all the clients
                #Problem?

                #What if someone adds a tile, and refreshes the database while multiple worlds are online. 
                #Well those worlds wont change, they will use the old tilesets
                #so its confusing but not problem


                utils.loadMapImage(worldDict, self.database)
                utils.loadEnemyHerds(worldDict, self.database)
                utils.loadStaticEntities(worldDict, self.database)
                utils.printWorldDictionary(worldDict)
            print(f"Loaded Worlds!")



    

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