# enemy class file
import pygame
import math
from settings import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y, player):
        self.game = game
        self._layer = enemy_layer

        # add to the relevant groups
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        # create the enemy image
        self.image = pygame.image.load('img/enemy.png')
        self.og_image = self.image.copy()

        # get the enemy's rectangle box thing
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # player
        self.player = player

        # set the enemy's direction
        self.direction = pygame.Vector2(1, 0)

        # get the position of the enemy
        self.position = self.rect.center

        # enemy's velocity
        self.yv = -enemy_speed

    # update the enemy
    def update(self):
        # move the enemy
        self.movement()

    # movement of the enemy
    def movement(self):
        # rotate the enemy
        self.rotate()

        # move the enemy towards the player
        self.position = self.direction * self.yv
        self.rect.center += self.position

    # rotate the enemy towards the player
    def rotate(self):
        position = self.rect.center
        rect = self.image.get_rect(center=position)

        # find the angle to rotate by
        dx, dy = self.player.rect.centerx - rect.centerx, rect.centery - self.player.rect.centery
        angle = int(math.degrees(math.atan2(dy, dx)) - 90)

        # rotate the enemy
        self.image = pygame.transform.rotozoom(self.og_image, angle, 1)
        self.rect = self.image.get_rect(center=position)

        # set the direction
        self.direction = pygame.Vector2(1, 0).rotate(-(angle - 90))

