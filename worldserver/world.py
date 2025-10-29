import base64
from enemyherd import EnemyHerd
from static_entity import StaticEntity
from staticEntityHole import StaticEntityHole

'''
every world is going to have a 2d array of tile ids to store world data?

'''

class World:
    def __init__(self):
        #read from the dataserver's world yml file, loaded in from JSON, can do .get("World-Name"), etc...
        self.worldDict = {}
        self.tilesDict = {}
        self.tileMapDict = {}
        self.staticsDict = {}

        self.enemyHerds = []
        self.staticHoles = []

        self.worldData = bytes() #decoded into tile IDs
        self.width = 0
        self.height = 0

    def tick(self, handler):
        #getting called 60 Times per second!

        # PRANAV IN HERE
        self.checkWorldTrigger()



        for enemyHerd in self.enemyHerds:
            enemyHerd.tick(handler)

        for hole in self.staticHoles:
            if not hole.filled:
                #add an entity, set it to filled
                for entry in self.staticsDict:
                    if entry.get('code-name') == hole.type:
                        print(entry)
                        print(f"x {hole.x} y {hole.y}")

                        etype = entry.get('code-name')
                        health = entry.get('health')
                        level = entry.get('Level')
                        handler.em.addEntity(StaticEntity(etype, hole.x, hole.y, health, level))
                        hole.filled = True



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
        self.worldDict = d.get("world")
        self.tilesDict = d.get("tiles")
        self.tileMapDict = d.get("tileMap")
        self.staticsDict = d.get("statics")
        
        #okay so we store all of the data in the worldserver so we can give it out



        worldData = self.worldDict.get("world-data")

        self.worldData = base64.b64decode(worldData)
        self.width = self.worldDict.get("world-width")
        self.height = len(self.worldData) // self.width   # using // is integer division
        
        #okay so we loaded world data, width and height, stored dictionaries to send to clients, now load enemy herds and entities

        print("LOADING ENEMY HERDS")

        print(self.worldDict.get("EnemyHerds"))
        for enemyHerd in self.worldDict.get("EnemyHerds"):
            herd = EnemyHerd(enemyHerd)
            self.enemyHerds.append(herd)
        



        world_statics = self.worldDict.get("StaticEntities")

        print(f"statics DB: {self.staticsDict}")
        print(f"static_entities.yml: {world_statics}")
        
        for eTypes in world_statics:
            print(f"\t{eTypes}")
            for (x, y) in world_statics[eTypes]:
                self.staticHoles.append(StaticEntityHole(eTypes, x, y))

                

    def checkWorldTrigger(self):
        #being called 60 times per second
        #Not the most efficient way to do, probably event system instead, but hey
        #checks if any player is in trigger
        pass