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
        self.enemyHerds = []
        self.worldData = bytes() #decoded into tile IDs
        self.width = 0
        self.height = 0

    def tick(self, handler):
        #getting called 60 Times per second!

        # PRANAV IN HERE
        self.checkWorldTrigger()



        for enemyHerd in self.enemyHerds:
            enemyHerd.tick(handler)



    def printWorldData(self):
        """
        Debug routine to print out world layout and tile mappings.

        Prints:
        - World dimensions.
        - Tile ID values in a grid matching world layout.
        - Descriptions of known tile IDs to names.
        """
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
        for enemyHerd in d.get("world").get("EnemyHerds"):
            herd = EnemyHerd(enemyHerd, self)


        #once all of the herds are instantiated, they they should all add themselves to the list given their is no errors
        #have them print their names
        # for h in self.enemyHerds:
        #     h.printInfo()

    def checkWorldTrigger(self):
        #being called 60 times per second
        #Not the most efficient way to do, probably event system instead, but hey
        #checks if any player is in trigger
        pass