'''
Okay so the entity class is going to be used to represent every type of non player entity, this is not an abstract
class, every monster is an instanceof this class. Although they have different hp, defence, damage, dodge chance, etc..
every entity is of this class
'''

class Entity:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    def tick(self):
        pass
