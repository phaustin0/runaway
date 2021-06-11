# player class file
import pygame
import math
from settings import *
from bullet import *


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self._layer = player_layer
        self.shooter_type = 'player'

        # add to the relevant groups
        self.groups = self.game.all_sprites, self.game.players
        pygame.sprite.Sprite.__init__(self, self.groups)

        # create the player's image
        self.image = pygame.image.load('img/player.png').convert()
        self.og_image = self.image.copy()

        # get the players rectangele box thing
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)

        # set the player's initial vertical and horizontal velocity to 0
        self.xv = 0
        self.yv = 0

        # direction of player
        self.direction = pygame.Vector2(1, 0)

        # shootings bullets
        self.bullet_timer = player_bullet_shoot_interval
        self.can_shoot = True

        # set players health
        self.health = player_max_health

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

        # check for any collisions
        self.check_collisions()
        
        # draw the shoot bar
        self.draw_shoot_bar()
        pygame.display.update()

        # destroy if health is less than 0
        if self.health <= 0:
            self.kill()

    # player movement
    def movement(self):
        # rotate player
        self.rotate()

        # lower the bullet timer
        self.bullet_timer -= 1 if not self.can_shoot else 0
        if self.bullet_timer < 0:
            self.can_shoot = True
            self.bullet_timer = player_bullet_shoot_interval

        # keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:  # up
#             for sprite in self.game.all_sprites:
#                 sprite.rect.y += player_speed
            self.yv -= player_speed
        elif keys[pygame.K_s]:  # down
#             for sprite in self.game.all_sprites:
#                 sprite.rect.y -= player_speed
            self.yv += player_speed
        if keys[pygame.K_a]:  # left
#             for sprite in self.game.all_sprites:
#                 sprite.rect.x += player_speed
            self.xv -= player_speed
        elif keys[pygame.K_d]:  # right
#             for sprite in self.game.all_sprites:
#                 sprite.rect.x -= player_speed
            self.xv += player_speed

        # mouse
        mouse_press = pygame.mouse.get_pressed()[0]
        if mouse_press:
            if self.can_shoot:
                Bullet(self.game, self, player_bullet_colour, player_bullet_speed, player_bullet_damage, self.direction)
                self.can_shoot = False

    # rotate player
    def rotate(self):
        player_pos = self.rect.center
        player_rect = self.image.get_rect(center=player_pos)
        
        # find the angle to rotate by
        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - player_rect.centerx, player_rect.centery - my
        angle = int(math.degrees(math.atan2(dy, dx)) - 90)

        self.image = pygame.transform.rotate(self.og_image, angle)
        self.rect = self.image.get_rect(center=player_pos)

        self.direction = pygame.Vector2(1, 0).rotate(-(angle + 90))

    # draw the shoot bar
    def draw_shoot_bar(self):
        angle = ((player_bullet_shoot_interval - self.bullet_timer) / player_bullet_shoot_interval) * math.pi
        pygame.draw.arc(self.game.screen, light_grey, (20, height - 90, 150, 150), 0, math.pi, 20)
        pygame.draw.arc(self.game.screen, dark_grey, (20, height - 90, 150, 150), 0, angle, 20)

    # check for collisions
    def check_collisions(self):
        # check if collided with enemy
        enemy_hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if enemy_hits:
            self.kill()
            self.game.playing = False

        # check if hit with a bullet
        bullet_hits = pygame.sprite.spritecollide(self, self.game.enemy_bullets, True)
        if bullet_hits:
            for bullet in bullet_hits:
                self.health -= bullet.damage

