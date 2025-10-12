class EntityManager:
    def __init__(self):
        self.items = []    #this is a list of the entity objects
        self.indices = {}  #this is a dict linking their IDs with the indices in the items list

    def getNumberOfEntities(self):
        return len(self.entities)

    def addEntity(self, e):
        #okay so this function is adding an entity, e to our Manager
        #it is O(1)
        if e.id in self.indices:
            raise ValueError(f"Entity {e.id} already exists")
        self.indices[e.id] = len(self.items)
        self.items.append(e)

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
