# powerups file
import pygame
from quid import *


# base powerup class
class Powerup:
    cost = 5
    def __init__(self, player):
        self.quid = player.quid
        
    def buy_powerup(self):
        can_buy = self.quid.deduct_quid(self.cost)
        if can_buy:
            self.increase_cost()
        return can_buy

    @classmethod
    def increase_cost(cls):
        cls.cost += 5

