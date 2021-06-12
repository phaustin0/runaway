# quid class file
import pygame


class Quid:
    def __init__(self):
        self._value = 0

    # get the number of quid
    def get_quid(self):
        return self._value

    # adding quid
    def add_quid(self, amount):
        self._value += amount

    # deducting quid
    def deduct_quid(self, amount):
        if self._value - amount < 0:
            return False
        self._value -= amount
        return True

