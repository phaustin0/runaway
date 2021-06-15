# player class file
import pygame
import math
from settings import *
from bullet import *
from background import *
from quid import *
from enemy_spawner import *


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

        # create background
        self.bg = Background(self.game, "img/backgrounds/space_background.png")

        # arrow
        self.arrow = pygame.image.load('img/arrow.png')
        self.og_arrow = self.arrow.copy()

        self.arrow_rect = self.arrow.get_rect()

        # entering planet
        self.can_enter_planet = False
        self.is_in_planet = False

        # planet timer
        self.planet_timer = pygame.time.get_ticks()
        self.time_in_planet = 0

        # planet
        self.planet_image = pygame.image.load('img/planet.png')
        self.planet_rect = self.planet_image.get_rect()

        # quid
        self.quid = Quid()
        self.quid_image = pygame.image.load('img/quid.png')
        self.quid_rect = self.quid_image.get_rect()

        # font
        self.font = pygame.font.SysFont('Comic Sans MS', 50, True)

        # kills
        self.kill_image = pygame.image.load('img/enemy_kill.png')
        self.kill_rect = self.kill_image.get_rect()
        self.kills = 0  # number of kills

        # enemy spawner
        self.enemy_spawner = EnemySpawner(self.game, self)
        self.enemy_spawn_timer = pygame.time.get_ticks()

        # spawn an enemy first
        self.enemy_spawner.spawn_enemy()

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

        # reset entering planet
        self.can_enter_planet = False

        # planet logic if player is in planet
        self.planet_logic()

        # spawn enemies
        self.spawn_enemy()

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
        if keys[pygame.K_e]:
            self.can_enter_planet = True

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
        pygame.draw.rect(self.game.screen, dark_grey, (35, 80, 250, 25))
        pygame.draw.rect(self.game.screen, light_grey, (35, 80, self.bullet_timer / player_bullet_shoot_interval * 250, 25))
        gun_img = pygame.image.load('img/gun.png')
        gun_img_rect = gun_img.get_rect(center=(35 + 5, 80 + 14))
        self.game.screen.blit(gun_img, gun_img_rect)

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

    # draw arrow
    def draw_arrow(self):
        # get the nearest planet
        distance = float('inf')
        nearest_planet = None
        for planet in self.game.planets:
            current_distance = math.sqrt(abs(planet.rect.centerx - self.rect.centerx) ** 2 + abs(planet.rect.centery - self.rect.centery) ** 2)
            if distance > current_distance:
                nearest_planet = planet
                distance = current_distance

        # find the angle
        try:
            self.arrow_rect.center = (350, 60)
            arrow_pos = self.arrow_rect.center
            dx, dy = nearest_planet.rect.centerx - self.rect.centerx, self.rect.centery - nearest_planet.rect.centery
            angle = int(math.degrees(math.atan2(dy, dx)) - 90)

            self.arrow = pygame.transform.rotate(self.og_arrow, angle)
            self.arrow_rect = self.arrow.get_rect(center=arrow_pos)
            self.game.screen.blit(self.arrow, self.arrow_rect)
        except Exception:
            return

    # draw the amount of quid
    def draw_quid(self):
        num_of_quid = str(self.quid.get_quid())
        text_surface = self.font.render(num_of_quid, True, (241, 178, 22))
        text_rect = text_surface.get_rect()
        text_rect.topright = (width - 25, 12)
        self.quid_rect.topright = (text_rect.left - 15, 25)
        self.game.screen.blit(text_surface, text_rect)
        self.game.screen.blit(self.quid_image, self.quid_rect)

    # draw the amount of kills in the planet
    def draw_kills(self):
        if self.is_in_planet or not self.is_in_planet:  # if in planet, then draw the thing
            text_surface = self.font.render(str(self.kills), True, (96, 0, 0))
            text_rect = text_surface.get_rect()
            text_rect.topright = (self.quid_rect.left - 40, 12)
            self.kill_rect.topright = (text_rect.left - 15, 25)
            self.game.screen.blit(text_surface, text_rect)
            self.game.screen.blit(self.kill_image, self.kill_rect)

    # draw planet bar
    def draw_planet_bar(self):
        if self.is_in_planet:
            pygame.draw.rect(self.game.screen, darkest_grey, (35, 135, 250, 25))
            pygame.draw.rect(self.game.screen, darker_grey, (35, 135, (player_time_in_planet - (self.time_in_planet / 1000)) / player_time_in_planet * 250, 25))
            self.planet_rect.center = (42, 150)
            self.game.screen.blit(self.planet_image, self.planet_rect)

    # enter planet
    def enter_planet(self, planet):
        if self.can_enter_planet:
            self.is_in_planet = True
            planet_colour = planet.colour
            path = f"img/backgrounds/{planet_colour}_background.png"
            self.bg.change_background(path)
            self.planet_timer = pygame.time.get_ticks()
            self.enemy_spawn_timer = pygame.time.get_ticks() - enemy_spawn_interval * 1000

            # destroy all planets when entering one
            planet.kill()
            for sprite in self.game.all_sprites:
                if sprite in self.game.enemies or sprite in self.game.planets:
                    sprite.kill()

    # planet logic
    def planet_logic(self):
        if self.is_in_planet:
            self.time_in_planet = pygame.time.get_ticks() - self.planet_timer
            if self.time_in_planet > player_time_in_planet * 1000:  # remove player from planet
                path = "img/backgrounds/space_background.png"
                self.bg.change_background(path)
                self.is_in_planet = False
                for sprite in self.game.enemies:
                    sprite.kill()

    # spawn enemy
    def spawn_enemy(self):
        time_passed = pygame.time.get_ticks() - self.enemy_spawn_timer
        if time_passed >= enemy_spawn_interval * 1000:
            self.enemy_spawner.spawn_enemy()
            self.enemy_spawn_timer = pygame.time.get_ticks()

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

        # check if player is on a planet
        planet_hits = pygame.sprite.spritecollide(self, self.game.planets, False)
        if planet_hits:
            self.enter_planet(planet_hits[0])

