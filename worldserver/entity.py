'''
    Every entity in our game, both static, monsters and bosses, have a unique ID so the server can identify them, a
    type, which details the kind of entity, could be 'SlimeBoss', 'blue-slime', 'skeleton', 'tree' or even 'crop'



'''


class Entity:
    def __init__(self, type, x, y):
        self.UUID = None
        self.type = type
        self.x = x
        self.y = y

    def tick(self):
        pass
