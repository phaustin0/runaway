# enemy class file
import pygame
import math
from settings import *
from bullet import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y, player):
        self.game = game
        self._layer = enemy_layer
        self.shooter_type = 'enemy'

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

        # shooting bullets
        self.bullet_timer = enemy_bullet_shoot_interval
        self.can_shoot = True

        # enemy health
        self.target_health = enemy_max_health
        self.current_health = enemy_max_health

    # update the enemy
    def update(self):
        # move the enemy
        self.movement()

        # lower the bullet timer
        self.bullet_timer -= 1 if not self.can_shoot else 0
        if self.bullet_timer < 0:
            self.bullet_timer = enemy_bullet_shoot_interval
            self.can_shoot = True

        # shoot
        if self.can_shoot:
            Bullet(self.game, self, enemy_bullet_colour, enemy_bullet_speed, enemy_bullet_damage, -self.direction)
            self.can_shoot = False

        # check for collisions
        self.check_collisions()

        # destroy when health is less than zero
        if self.target_health <= 0:
            self.kill()

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

    # damage enemy
    def damage(self, amount):
        self.target_health -= amount

    # check for collisions
    def check_collisions(self):
        # check if hit by player bullet
        bullet_hits = pygame.sprite.spritecollide(self, self.game.player_bullets, True)
        if bullet_hits:
            self.damage(bullet_hits[0].damage)

    # draw health bar
    def draw_health_bar(self):
        transition_width = 0
        transition_colour = red
        health_animation_speed = 2

        if self.current_health < self.target_health:
            self.current_health += health_animation_speed
            transition_width = int((self.target_health - self.current_health) / enemy_max_health * 150)
            transition_colour = green
        if self.current_health > self.target_health:
            self.current_health -= health_animation_speed
            transition_width = int((self.current_health - self.target_health) / enemy_max_health * 100)
            transition_colour = yellow

        health_rect = pygame.Rect(self.rect.centerx - 75, self.rect.bottom + 10, self.target_health / (enemy_max_health / 150), 25)
        transition_rect = pygame.Rect(health_rect.right, self.rect.bottom + 10, transition_width, 25)

        if self.target_health != enemy_max_health:
            pygame.draw.rect(self.game.screen, dark_grey, (self.rect.centerx - 75, self.rect.bottom + 10, 150, 25))
            pygame.draw.rect(self.game.screen, red, health_rect)
            pygame.draw.rect(self.game.screen, transition_colour, transition_rect)
            heart_img = pygame.image.load('img/heart.png')
            heart_img_rect = heart_img.get_rect(center=(health_rect.left + 12, health_rect.centery))
            self.game.screen.blit(heart_img, heart_img_rect)

