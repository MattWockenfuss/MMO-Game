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

            spawnCount = 0
            if isinstance(self.herdSize, list):
                if self.currentCount < self.herdSize[0]:
                    spawnCount = random.randint((self.herdSize[0] - self.currentCount), self.herdSize[1])
                else:
                    spawnCount = random.randint(0, self.herdSize[1] - self.currentCount)
            else:
                spawnCount = random.randint(self.currentCount, self.herdSize)

            print(f"Spawning {spawnCount} Entities!")

            for i in range(spawnCount):
                x = random.randint((self.coords[0] - self.radius) * 64, (self.coords[0] + self.radius) * 64)
                y = random.randint((self.coords[1] - self.radius) * 64, (self.coords[1] + self.radius) * 64)
                
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
                self.currentCount += 1





    def printInfo(self):
        print(f"EnemyHerd {self.name}")
        print(f"\tCoords {self.coords}")
        print(f"\tRadius {self.radius}")
        print(f"\tHerdSize {self.herdSize}")
        print(f"\tCooldown {self.cooldown}")
        print(f"\tEnemyType {self.enemyType}")
        print(f"\tLevel {self.Level}")
        print(f"\tHealth {self.Health}")
        print(f"\tAttack {self.Attack}")
        print(f"\tAttackSpeed {self.AttackSpeed}")
        print(f"\tDodgeChance {self.DodgeChance}")
        print(f"\tCriticalChance {self.CriticalChance}")
        print(f"\tMovementSpeed {self.MovementSpeed}")
        print(f"\tVisionRadius {self.VisionRadius}")
        print(f"\tMovementType {self.MovementType}")

        print(f"Cooldown Timer: {self.cooldown}, current {self.cooldownTimer}")