"""
worldserver/enemy.py

Enemy class represents all monster-type entities in the MMO game, inheriting from the base Entity class.

Responsibilities:
- Extend Entity by adding combat and gameplay related attributes such as level, health, attack stats, movement,
  and detection abilities.
- Represent all kinds of enemies including bosses and regular monsters.
- Provide a framework for per-tick behavior updates via the tick() method (to be extended or overridden).
"""

'''
An Enemy is a child of the Entity object. Every enemy has x and y coordinates and an ID,
but they also have a variety of other attributes to define their combat and gameplay features.
They represent all monster types the player can attack, including bosses and mobs.
'''

from entity import Entity


class Enemy(Entity):
    def __init__(self, etype, x, y, level, health, attack, attackSpeed, dodgeChance, criticalChance, movementSpeed, visionRadius, size, movementType):
        super().__init__(etype, x, y)

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
        self.size = size
        self.movementType = movementType

        print(f"NEW ENEMY Type: {self.type} at ({self.x}, {self.y}), Level:{self.level}, Health:{self.health}, Attack:{self.attack}")




    def tick(self):
        """
        Per-tick update method for enemy behavior.

        Intended to be extended or overridden to implement enemy actions per server tick.
        Currently does nothing.
        """
        #print(f"{self.type}, ({self.x}, {self.y}), {self.level}, {self.health}")
        pass