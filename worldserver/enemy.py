import entity as Entity

'''
    An Enemy is a child of the Entity object, every enemy has an x and y coordinate and an ID, but they also have a bunch of other attributes. They are used to represent
    every type of monster in the game that the player is going to be able to attack. This could be bosses, or all of the different types of enemies.




'''


class Enemy(Entity):
    def __init__(self, id, type, x, y, level, health, attack, attackSpeed, dodgeChance, criticalChance, movementSpeed, visionRadius, movementType):
        super(id, type, x, y)

        self.level = level
        self.health = health
        self.attack = attack
        self.attackSpeed = attackSpeed
        self.dodgeChance = dodgeChance
        self.criticalChance = criticalChance
        self.movementSpeed = movementSpeed
        self.visionRadius = visionRadius
        self.movementType = movementType

        print(f"NEW ENEMY {self.type}, ({self.x}, {self.y}), {self.level}, {self.health}")




    def tick(self):
        print(f"{self.type}, ({self.x}, {self.y}), {self.level}, {self.health}")
