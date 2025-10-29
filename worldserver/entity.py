"""
worldserver/entity.py

Base Entity class representing any game object in the MMO world.

Responsibilities:
- Provide a unique identifier (UUID) for server-side entity tracking.
- Store entity type information to differentiate kinds of entities
  such as monsters (e.g., 'SlimeBoss', 'blue-slime', 'skeleton') or static objects ('tree', 'crop').
- Maintain entity position coordinates (x, y) within the game world.
- Define a tick() method intended to be overridden for per-tick entity behavior updates.
"""

'''
Every entity in our game, including statics, monsters, and bosses,
has a unique ID so the server can identify them, a type describing
the kind of entity (like 'SlimeBoss', 'blue-slime', 'skeleton', 'tree', or 'crop').
'''


class Entity:
    """
    Base entity class for all game objects.

    Attributes:
        UUID (str or None): Unique identifier assigned by the EntityManager.
        type (str): Identifier string describing the entity kind.
        x (int or float): Horizontal position coordinate in the world.
        y (int or float): Vertical position coordinate in the world.
    """
    def __init__(self, type, x, y):
        self.UUID = None
        self.type = type
        self.x = x
        self.y = y

    def tick(self):
        """
        Per-tick update method called by the server.

        Intended to be overridden by subclasses for entity-specific behavior.

        No operation in base class.
        """
        pass
