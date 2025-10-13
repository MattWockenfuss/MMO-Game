import base64
from enemyherd import EnemyHerd

'''
every world is going to have a 2d array of tile ids to store world data?

'''

class World:
    def __init__(self):
        #read from the dataserver's world yml file, loaded in from JSON, can do .get("World-Name"), etc...
        self.worldDict = {}
        self.tilesDict = {}
        self.enemyHerds = []
        self.worldData = bytes() #decoded into tile IDs
        self.width = 0
        self.height = 0

    def tick(self, handler):
        for enemyHerd in self.enemyHerds:
            enemyHerd.tick(handler)



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

        #now load all of the enemy data
        #how do we want to store this?
        #well the world is going to have a list of entity herds, each entity herd has a variety of attributes
        for enemyHerd in d.get("world").get("enemyHerds"):
            herd = EnemyHerd(enemyHerd, self)


        #once all of the herds are instantiated, they they should all add themselves to the list given their is no errors
        #have them print their names
        # for h in self.enemyHerds:
        #     h.printInfo()