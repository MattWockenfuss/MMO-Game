from entity import Entity

class StaticEntity(Entity):
    def __init__(self, type, x, y, health, level):
        super().__init__(type, x, y)

        self.health = health
        self.level = level

        print(f"NEW STATIC ENTITY CREATED AT ({x}, {y})")