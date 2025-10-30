"""
worldserver/entitymanage.py

EntityManager class manages game entities within the MMO world server.

Responsibilities:
- Store and organize all active entity objects in the game world.
- Maintain fast lookup from entity UUIDs to their storage indices.
- Support adding, retrieving, and removing entities efficiently.
- Broadcast new enemy entity creation to connected clients.
- Advance entity state by ticking each entity every server tick.
- Generate unique UUIDs for entities.
"""

import random, string
from enemy import Enemy
from static_entity import StaticEntity

class EntityManager:
    """
    Manager for all entities in the game world.

    Attributes:
        items (list): List of entity objects currently active.
        indices (dict): Maps entity UUIDs to their indices in the items list.
        handler (Handler): Reference to main server handler for accessing subsystems.
    """
    def __init__(self):
        #items is the list of actual entity objects
        #indices is a dictionary, linking uuids to the indices in the list

        self.items = []  
        self.indices = {}

        self.handler = None

    def getNumberOfEntities(self):
        return len(self.entities)

    """
        Add a new entity to the manager.

        Assigns a generated unique UUID, updates indices mapping,
        appends to internal list, and broadcasts new enemy entities to clients.

        Args:
            e (Entity): Entity instance to add.
    """
    def addEntity(self, e):
        e.UUID = self.generateUUID()
        self.indices[e.UUID] = len(self.items)
        self.items.append(e)

        #we also need to tell the clients about this entity? how?

        if isinstance(e, Enemy):
            p = {
                "uuid": e.UUID,
                "type": e.type,
                "x": e.x,
                "y": e.y,
                "level": e.level,
                "health": e.health,
                "attack": e.attack,
                "attackSpeed": e.attackSpeed,
                "dodgeChance": e.dodgeChance,
                "criticalChance": e.criticalChance,
                "movementSpeed": e.movementSpeed,
                "visionRadius": e.visionRadius,
                "size": e.size,
                "movementType": e.movementType
            }
            self.handler.csm.broadcast("Enemy", p)
        elif isinstance(e, StaticEntity):
            p = {
                "uuid": e.UUID,
                "type": e.type,
                "x": e.x,
                "y": e.y,
                "level": e.level,
                "health": e.health
            }
            print(f"Telling all players of a new Static Entity -> {p}")
            self.handler.csm.broadcast("StaticEntity", p)


    def getByIndex(self, i):
        return self.items[i]
    
    def getByID(self, eid):
        """
        Retrieve entity by its UUID.

        Args:
            eid (str): UUID of the entity.

        Returns:
            Entity or None: Entity if found, else None.
        """
        idx = self.indices.get(eid)
        return None if idx is None else self.items[eid]
    
    def removeByID(self, eid):
        """
        Remove an entity by UUID.

        Efficiently removes entity by swapping with last entity in the list to fill the gap.

        Args:
            eid (str): UUID of the entity to remove.

        Returns:
            bool: True if entity was removed, False if not found.
        """
        idx = self.indices.pop(eid, None)
        if idx is None:
            return False
        
        lastIdx = len(self.items) - 1
        if idx != lastIdx:
            #move the last guy into the hole
            last_entity = self.items[lastIdx]
            self.items[idx] = last_entity
            self.indices[last_entity.id] = idx

        self.items.pop
        return True

    def tick(self, handler):
        for entity in self.items:
            entity.tick()

    def generateUUID(self):
        """
        Generate a unique 8-character alphanumeric UUID for entities.

        Ensures no collision with existing entity UUIDs.

        Returns:
            str: Unique UUID string.
        """
        characterPool = string.ascii_letters + string.digits
        while True:
            key = ''.join(random.choice(characterPool) for i in range(8))
            if key not in self.indices: return key