import random
from enemy import Enemy


class EnemyHerd:
    def __init__(self, dictionary, world):
        print(f"Creating new Enemy Herd!")
        print(f"From {dictionary}")
        # for keys, values in dictionary.items():
        #     print(f"{keys} -> {values}")
        
        self.name = dictionary.get("name")
        self.coords = dictionary.get("coords")
        self.radius = dictionary.get("radius")
        self.herdSize = dictionary.get("herdSize")
        self.cooldown = dictionary.get("cooldown")
        self.enemyType = dictionary.get("enemyType")
        self.Level = dictionary.get("Level")
        self.Health = dictionary.get("Health")
        self.Attack = dictionary.get("Attack")
        self.AttackSpeed = dictionary.get("Attack-Speed")
        self.DodgeChance = dictionary.get("Dodge-Chance")
        self.CriticalChance = dictionary.get("Critical-Chance")
        self.MovementSpeed = dictionary.get("Movement-Speed")
        self.VisionRadius = dictionary.get("Vision-Radius")
        self.MovementType = dictionary.get("Movement-Type")

        self.cooldownTimer = 0
        self.currentCount = 0






        world.enemyHerds.append(self)

    def getRandomAttribute(self, attribute):
        #print(f"Testing Attribute for {attribute}")
        if isinstance(attribute, list):
            #print(f"{attribute} is a list!")
            return random.randint(attribute[0], attribute[1])
        else:
            #print(f"{attribute} is NOT a list!")
            return attribute

    def tick(self, handler):
        self.cooldownTimer -= 1
        #alright so we are ticking the enemyHerd, we want to check if the herd has enough members, and if not, spawn on cooldown
        if self.cooldownTimer <= 0:
            self.cooldownTimer = self.getRandomAttribute(self.cooldown)
            #print(f"Attempting to Spawn '{self.name}', Cooldown: {self.cooldown[0]} => {self.cooldown[1]}: {self.cooldownTimer}")

            #okay so herdSize is either a number or a range,
                
            # if range and current is less than min, then pick a number between current and max, spawn that many
            # if number, and current count is less than number, then pick a random number between current and number, spawn that many

            # So we can refactor the function, 

            spawnCount = self.getRandomAttribute(self.herdSize) - self.currentCount

            #okay so spawncount is either equal to the number in the config, or a random number in between min and max, now subtract currentCount
            #this way we shouldnt ever go over
            #if we have 3 and the range is 5 to 10, our random number could be
            #           5 - 3 = 2 spawnCounts so we will have 5
            #           10 - 3 = 7 spawnCounts so we will have 10

            print(f"Spawning {spawnCount} Entities!")

            for i in range(spawnCount):
                x = random.randint(self.coords[0] - self.radius, self.coords[0] + self.radius)
                y = random.randint(self.coords[1] - self.radius, self.coords[1] + self.radius)
                
                level = self.getRandomAttribute(self.Level)
                health = self.getRandomAttribute(self.Health)
                attack = self.getRandomAttribute(self.Attack)
                attackSpeed = self.getRandomAttribute(self.AttackSpeed)
                dodgeChance = self.getRandomAttribute(self.DodgeChance)
                criticalChance = self.getRandomAttribute(self.CriticalChance)
                movementSpeed = self.getRandomAttribute(self.MovementSpeed)
                visionRadius = self.getRandomAttribute(self.VisionRadius)

                e = Enemy(self.enemyType, x, y, 
                    level, health, attack, attackSpeed, 
                    dodgeChance, criticalChance, movementSpeed, 
                    visionRadius, self.MovementType)
                handler.em.addEntity(e)





    def printInfo(self):
        print(f"EnemyHerd {self.name}")
        print(f"Coords {self.coords}")
        print(f"Radius {self.radius}")
        print(f"HerdSize {self.herdSize}")
        print(f"Cooldown {self.cooldown}")
        print(f"EnemyType {self.enemyType}")
        print(f"Level {self.Level}")
        print(f"Health {self.Health}")
        print(f"Attack {self.Attack}")
        print(f"AttackSpeed {self.AttackSpeed}")
        print(f"DodgeChance {self.DodgeChance}")
        print(f"CriticalChance {self.CriticalChance}")
        print(f"MovementSpeed {self.MovementSpeed}")
        print(f"VisionRadius {self.VisionRadius}")
        print(f"MovementType {self.MovementType}")

        self.cooldownTimer = random.randint(self.cooldown[0], self.cooldown[1])
        print(f"Cooldown Timer: {self.cooldown[0]} => {self.cooldown[1]}: {self.cooldownTimer}")