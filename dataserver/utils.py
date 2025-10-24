import base64
import yaml
from PIL import Image

def loadMapImage(worldDict, database): 
    #item is the dictionary for this world, this function reads the image file and loads data into world dict of their ids
    #print(worldDict)
    subfolder = worldDict.get("folderName")
    tilemapName = worldDict.get("Tile-Map")

    im = Image.open(f"configs/worlds/{subfolder}/{tilemapName}")
    #print(im.format, im.size, im.mode)
    #print(f"{im.width} x {im.height}")
    im = im.convert("RGB")

    #alright so we know the width and height of the world, now lets load it in, and store it in a byte array
    tiles = bytearray(im.width * im.height)
    
    for y in range(im.height):
        for x in range(im.width):
            idx = y * im.width + x
            point = (x, y)
            r, g, b = im.getpixel(point)

            for tile in database["tiles"]:
                if f"#{r:02x}{g:02x}{b:02x}" == tile.get("map-color"):
                    tiles[idx] = tile.get("id")
                    break
            else:
                tiles[idx] = 5 #the void tile, ehh

    world_data = bytes(tiles)
    
    worldDict["world-data"] = base64.b64encode(world_data).decode("utf-8")   #add it to the database, probably change this later?
    worldDict["world-width"] = im.width
    


    

    for y in range(im.height):
        for x in range(im.width):
            point = (x,y)
            r , g, b = im.getpixel(point)
            #print(f"#{r:02x}{g:02x}{b:02x}")   #python formatting, L is the format specifier, x means hexadecimal and 02 means pad with 0s to be atleast 2 wide  


def loadEnemyHerds(worldDict, database):
    subfolder = worldDict.get("folderName")
    path = f"configs/worlds/{subfolder}/enemy_herds.yml"

    try:
        herdsyml = readYML(path)
        #print(herdsyml)
        worldDict["EnemyHerds"] = herdsyml
    except FileNotFoundError:
        print(f"\t[SKIPPING] 'configs/worlds/{subfolder}/enemy_herds.yml' NOT FOUND, SKIPPING")
    except Exception as e:
        print(f"\t[ERROR] Error Loading {path}, {e}")

def loadStaticEntities(worldDict, database):
    #okay we have a library of static entities, print them
    #print(f"DATABASE OF STATICS: {database["statics"]}")

    subfolder = worldDict.get("folderName")
    path = f"configs/worlds/{subfolder}/static_entities.yml"

    try:
        static_entities = readYML(path)
        #print(f"STATIC ENTITIES TO ADD: {static_entities}")
        worldDict["StaticEntities"] = static_entities
    except FileNotFoundError:
        print(f"\t[SKIPPING] 'configs/worlds/{subfolder}/static_entities.yml' NOT FOUND, SKIPPING")
    except Exception as e:
        print(f"\t[ERROR] Error Loading {path}, {e}")

    

def printWorldDictionary(dict):
    #this function prints the world dictionary, essentially skipping the world data
    #print(dict)
    name = dict.get("World-Name")
    print(name)
    for tag in dict:
        if tag == "world-data":
            print(f"\t{tag}: ...")
            continue
        print(f"\t{tag}: {dict[tag]}")

def readYML(path):
    #print(f"[READ-YML] READING {path}")
    with open(path) as stream:
        try:
            data = yaml.safe_load(stream)
            return data 
        except yaml.YAMLError as exc:
            print(exc)