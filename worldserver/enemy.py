from entity import Entity

'''
    An Enemy is a child of the Entity object, every enemy has an x and y coordinate and an ID, but they also have a bunch of other attributes. They are used to represent
    every type of monster in the game that the player is going to be able to attack. This could be bosses, or all of the different types of enemies.




'''



class Enemy(Entity):
    def __init__(self, type, x, y, level, health, attack, attackSpeed, dodgeChance, criticalChance, movementSpeed, visionRadius, movementType):
        super().__init__(type, x, y)

        #Everything about an Entity is defined here for simplicity, even if they dont use it, dont add to the object later.
        #the only exception here is the UUID, which is added for all entities by the entity manager

        #self.UUID = ...
        self.level = level
        self.health = health
        self.attack = attack
        self.attackSpeed = attackSpeed
        self.dodgeChance = dodgeChance
        self.criticalChance = criticalChance
        self.movementSpeed = movementSpeed
        self.visionRadius = visionRadius
        self.movementType = movementType

        print(f"NEW ENEMY Type: {self.type} at ({self.x}, {self.y}), Level:{self.level}, Health:{self.health}, Attack:{self.attack}")




    def tick(self):
        #print(f"{self.type}, ({self.x}, {self.y}), {self.level}, {self.health}")
        pass