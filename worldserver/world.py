import base64
'''
every world is going to have a 2d array of tile ids to store world data?

'''

class World:
    def __init__(self):
        #read from the dataserver's world yml file, loaded in from JSON, can do .get("World-Name"), etc...
        self.worldDict = {}
        self.tilesDict = {}
        self.worldData = bytes() #decoded into tile IDs
        self.width = 0
        self.height = 0

    def tick(self, handler):
        pass



    def printWorldData(self):
        print(f"{self.width} x {self.height} = {len(self.worldData)}")

        for y in range(self.height):
            for x in range(self.width):
                idx = y * self.width + x
                print(f"{self.worldData[idx]} ", end="")
            print("")

        #alright lets print the tiles to match
        print(f"Where,")
        for tile in self.tilesDict:
            print(f'{tile.get("id")} >> "{tile.get("name")}"')


    def setWorldData(self, d):
        #these are both dictionaries
        world = d.get("world")
        tiles = d.get("tiles")
        #print("okay got world and tiles")
        worldData = world.get("world-data")
        #print(worldData)
        self.worldData = base64.b64decode(worldData)
        self.width = world.get("world-width")
        self.height = len(self.worldData) // self.width   # using // is integer division
        #print("okay got worlddata and width and height")
        self.worldDict = world
        self.tilesDict = tiles
        #print(f"World Name: {self.worldDict.get("World-Name")}")
        #self.printWorldData()

