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
        self.target_health = player_max_health
        self.current_health = player_max_health

        # health bars
        self.health_rect = pygame.Rect(35, 25, self.current_health / player_max_health * 250, 25)
        self.transition_rect = pygame.Rect(self.health_rect.right, 25, 0, 25)

        # health timer
        self.health_timer = pygame.time.get_ticks()

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
        
        # heal player
        self.heal(player_heal_amount)

        # destroy if health is less than 0
        if self.target_health <= 0:
            self.kill()
            self.game.playing = False

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
            if self.rect.top < 50:
                for sprite in self.game.all_sprites:
                    sprite.rect.y += player_speed
            self.yv -= player_speed
        elif keys[pygame.K_s]:  # down
            if self.rect.bottom > height - 50:
                for sprite in self.game.all_sprites:
                    sprite.rect.y -= player_speed
            self.yv += player_speed
        if keys[pygame.K_a]:  # left
            if self.rect.left < 50:
                for sprite in self.game.all_sprites:
                    sprite.rect.x += player_speed
            self.xv -= player_speed
        elif keys[pygame.K_d]:  # right
            if self.rect.right > width - 50:
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= player_speed
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

    # heal the player
    def heal(self, amount):
        time_passed = pygame.time.get_ticks() - self.health_timer
        if time_passed > player_heal_time * 1000:
            self.target_health += amount
            self.health_timer = pygame.time.get_ticks()
        self.target_health = min(self.target_health, player_max_health)

    # draw the shoot bar
    def draw_shoot_bar(self):
        angle = ((player_bullet_shoot_interval - self.bullet_timer) / player_bullet_shoot_interval) * math.pi
        pygame.draw.arc(self.game.screen, light_grey, (20, height - 90, 150, 150), 0, math.pi, 20)
        pygame.draw.arc(self.game.screen, dark_grey, (20, height - 90, 150, 150), 0, angle, 20)

    # draw the health bar
    def draw_health_bar(self):
        transition_width = 0
        transition_colour = red
        health_animation_speed = 2

        if self.current_health < self.target_health:
            self.current_health += health_animation_speed
            transition_width = int((self.target_health - self.current_health) / player_max_health * 250)
            transition_colour = green

            self.health_rect = pygame.Rect(35, 25, self.current_health / player_max_health * 250, 25)
            self.transition_rect = pygame.Rect(self.health_rect.right, 25, transition_width, 25)
        if self.current_health > self.target_health:
            self.current_health -= health_animation_speed
            transition_width = -int((self.target_health - self.current_health) / player_max_health * 250)
            transition_colour = yellow

            self.health_rect = pygame.Rect(35, 25, self.target_health / player_max_health * 250, 25)
            self.transition_rect = pygame.Rect(self.health_rect.right, 25, transition_width, 25)

        pygame.draw.rect(self.game.screen, dark_grey, (35, 25, 250, 25))
        pygame.draw.rect(self.game.screen, red, self.health_rect)
        pygame.draw.rect(self.game.screen, transition_colour, self.transition_rect)
        heart_img = pygame.image.load('img/heart.png')
        heart_img_rect = heart_img.get_rect(center=(self.health_rect.left + 12, self.health_rect.centery))
        self.game.screen.blit(heart_img, heart_img_rect)

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
                self.target_health -= bullet.damage

                # reset the health timer
                self.health_timer = pygame.time.get_ticks()

