"""
worldserver/world.py

World class representing the MMO game world state.

Responsibilities:
- Stores world data as a 2D array of tile IDs decoded from base64 data.
- Maintains metadata about the world dimensions.
- Manages a list of enemy herds present in the world.
- Provides periodic updates through the tick() method called every server tick.
- Supports setting world data from a structured dictionary (e.g. loaded JSON/YAML from the data server).
- Includes debug printing utilities to output world data and tile mappings.
- Placeholder for trigger checking logic to detect player interactions with world events.

Dependencies:
- base64: To decode world data encoding.
- enemyherd.EnemyHerd: Enemy herd entity class representing groups of enemies.
"""

import base64
from enemyherd import EnemyHerd
from static_entity import StaticEntity
from staticEntityHole import StaticEntityHole

'''
every world is going to have a 2d array of tile ids to store world data?

'''

class World:
    def __init__(self):
        """
            Main game world representation.

            Attributes:
                worldDict (dict): Dictionary containing world metadata and config.
                tilesDict (dict): Dictionary mapping tile IDs to tile properties.
                enemyHerds (list): List of EnemyHerd instances in the world.
                worldData (bytes): Raw decoded tile data defining the world layout.
                width (int): Number of tiles horizontally.
                height (int): Number of tiles vertically.
        """
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


    """
        Debug routine to print out world layout and tile mappings.

        Prints:
        - World dimensions.
        - Tile ID values in a grid matching world layout.
        - Descriptions of known tile IDs to names.
    """
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

    """
    Initialize world data from a nested dictionary structure.

    Extracts:
    - base64-encoded worldData which is decoded into raw tile IDs.
    - World dimensions (width, height).
    - Tile dictionary describing tiles by ID.
    - Constructs EnemyHerd instances from enemy herd data within the world.

    Args:
        d (dict): Dictionary containing 'world' and 'tiles' data from the dataserver.
    """
    def setWorldData(self, d):
        #Store all of the data from the data server in our dictionaries
        self.worldDict = d.get("world")
        self.tilesDict = d.get("tiles")
        self.tileMapDict = d.get("tileMap")
        self.staticsDict = d.get("statics")



        #Okay, so stored all of the dictionaries needed, set the world data, including width and height

        worldData = self.worldDict.get("world-data")

        self.worldData = base64.b64decode(worldData)
        self.width = self.worldDict.get("world-width")
        self.height = len(self.worldData) // self.width   # using // is integer division
        


        #okay so we loaded world data, width and height, stored dictionaries to send to clients, now load enemy herds and entities
        for enemyHerd in self.worldDict.get("EnemyHerds"):
            herd = EnemyHerd(enemyHerd)
            self.enemyHerds.append(herd)
        


        # Next up, statics

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