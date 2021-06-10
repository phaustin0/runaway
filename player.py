# player class file
import pygame
import math
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self._layer = player_layer

        # add to the relevant groups
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        # create the player's image
        self.image = pygame.Surface([50, 50])
        self.image.fill(blue)
        self.og_image = self.image.copy()

        # get the players rectangele box thing
        self.rect = self.image.get_rect()
        self.rect.x = (width - 50) / 2
        self.rect.y = (height - 50) / 2

        # set the player's initial vertical and horizontal velocity to 0
        self.xv = 0
        self.yv = 0

    # update the player
    def update(self):
        # apply movement
        self.movement()

        # apply the velocity to the player
        self.rect.x += self.xv
        self.rect.y += self.yv

        # set the velocity to 0
        self.xv = 0
        self.yv = 0

    # player movement
    def movement(self):
        # rotate player
        self.rotate()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:  # up
            self.yv -= player_speed
        elif keys[pygame.K_s]:  # down
            self.yv += player_speed
        if keys[pygame.K_a]:  # left
            self.xv -= player_speed
        elif keys[pygame.K_d]:  # right
            self.xv += player_speed

    # rotate player
    def rotate(self):
        player_pos = self.rect.center
        player_rect = self.image.get_rect(center=player_pos)
        
        # find the angle to rotate by
        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - player_rect.centerx, player_rect.centery - my
        angle = int(math.degrees(math.atan2(dy, dx)))

        self.image = pygame.transform.rotozoom(self.og_image, angle, 1)
        self.rect = self.image.get_rect(center=player_pos)

