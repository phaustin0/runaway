# enemy spawning file
import pygame
from random import choice
from settings import *
from enemy import *


class EnemySpawner:
    def __init__(self, game, player):
        self.game = game
        self.positions = [
            (-100, -100),  # top left
            (width // 4, -100),  # top middle left
            (width // 2, -100),  # top middle
            (width // 4 * 3, -100),  # top middle right
            (width + 100, -100),  # top right
            (width + 100, height // 3),  # right middle top
            (width + 100, height // 3 * 2),  # right middle bottom
            (width + 100, height + 100),  # bottom right
            (width // 4 * 3, height + 100),  # bottom middle right
            (width // 2, height + 100),  # bottom middle
            (width // 4, height + 100),  # bottom middle left
            (-100, height + 100),  # bottom left
            (-100, height // 3 * 2),  # left middle bottom
            (-100, height // 2)  # left middle top
        ]
        self.player = player

    # choose a random position
    def get_random_position(self):
        return choice(self.positions)

    # spawn the enemy
    def spawn_enemy(self):
        # get the position for the enemy to spawn in
        x, y = self.get_random_position()

        # spawn the enemy
        Enemy(self.game, x, y, self.player, self.player.enemy_speed, self.player.enemy_bullet_shoot_interval, self.player.enemy_bullet_damage)

