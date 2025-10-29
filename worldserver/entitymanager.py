import random, string
from enemy import Enemy
from static_entity import StaticEntity

class EntityManager:
    def __init__(self):
        #items is the list of actual entity objects
        #indices is a dictionary, linking uuids to the indices in the list

        self.items = []  
        self.indices = {}

        self.handler = None

    def getNumberOfEntities(self):
        return len(self.entities)

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
        idx = self.indices.get(eid)
        return None if idx is None else self.items[eid]
    
    def removeByID(self, eid):
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
        characterPool = string.ascii_letters + string.digits
        while True:
            key = ''.join(random.choice(characterPool) for i in range(8))
            if key not in self.indices: return key