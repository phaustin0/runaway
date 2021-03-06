# bullet class file
import pygame
from settings import *

# bullet settings
bullet_layer = 3
bullet_time_to_kill = 1000


class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, shooter, colour, speed, damage, direction):
        self.game = game
        self.shooter = shooter
        self._layer = bullet_layer

        # add to the relevant groups
        if self.shooter.shooter_type == 'player':
            self.groups = self.game.all_sprites, self.game.player_bullets
        else:
            self.groups = self.game.all_sprites, self.game.enemy_bullets
        pygame.sprite.Sprite.__init__(self, self.groups)

        # set width and height
        self.width = 10
        self.height = 10

        # set bullet velocity and direction
        self.yv = -speed
        self.direction = direction

        # set the image of the bullet
        self.image = pygame.Surface([self.width, self.height])
        pygame.draw.circle(self.image, colour, (5, 5), 5)

        # get the rectangle of bullet
        self.rect = self.image.get_rect()
        self.rect.centerx = self.shooter.rect.centerx
        self.rect.centery = self.shooter.rect.centery

        # get position of the bullet
        self.pos = pygame.Vector2(self.rect.center)

        # set the time in which the bullet was instantiated
        self.start_time = pygame.time.get_ticks()

        # set the damage to inflict
        self.damage = damage

    # update bullet
    def update(self):
        # move towards the direction
        self.pos += -self.direction * self.yv
        self.rect.center = self.pos

        # check if enough time has passed and kill afterwards to prevent lag
        self.destroy()

    # destroy bullet
    def destroy(self):
        time_passed = pygame.time.get_ticks() - self.start_time
        if time_passed > bullet_time_to_kill:
            self.kill()

