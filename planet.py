# planet class file
import pygame
from random import *
from settings import *


# base planet class
class Planet(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = planet_layer

        # add to the relevant groups
        self.groups = self.game.all_sprites, self.game.planets
        pygame.sprite.Sprite.__init__(self, self.groups)

        # position of planet
        self.x = x
        self.y = y

        # colour of planet
        self.colour = choice(["blue", "green", "pink", "purple", "red", "yellow"])
        self.image_key = {
            "blue": pygame.image.load("img/planets/blue_planet.png"),
            "green": pygame.image.load("img/planets/green_planet.png"),
            "pink": pygame.image.load("img/planets/pink_planet.png"),
            "purple": pygame.image.load("img/planets/purple_planet.png"),
            "red": pygame.image.load("img/planets/red_planet.png"),
            "yellow": pygame.image.load("img/planets/yellow_planet.png")
        }

        # create the image of the planet
        self.image = self.image_key[self.colour]
        self.og_image = self.image.copy()

        # get the rectangle of the planet
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # put the planet on the screen
        self.game.screen.blit(self.image, self.rect)

        # rotating
        self.angle = 0
        self.rotation_speed = choice([-2, -1, 1, 2])

    # update the planet
    def update(self):
        # rotate the planet
        self.rotate()

        # check for collisions
        self.check_collisions()

    # rotate the planet
    def rotate(self):
        self.angle += self.rotation_speed
        if self.angle > 360:
            self.angle -= 360
        elif self.angle < -360:
            self.angle += 360
        planet_pos = self.rect.center
        self.image = pygame.transform.rotate(self.og_image, self.angle)
        self.rect = self.image.get_rect(center=planet_pos)

    # check for collisions
    def check_collisions(self):
        bullet_hits = pygame.sprite.spritecollide(self, self.game.enemy_bullets, True)
        bullet_hits = pygame.sprite.spritecollide(self, self.game.player_bullets, True)

