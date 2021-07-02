# Main file to handle all game logic
import pygame
import sys
from button import *
from settings import *
from player import *
from enemy import *
from powerups import *
from powerup_icon import *


# game class
class Game:
    def __init__(self):
        # initialise pygame
        pygame.init()

        # create screen
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)

        # create clock
        self.clock = pygame.time.Clock()

        # running variable for whether application is running
        self.running = True

        # playing variable for whether the game is being played
        self.playing = False

        # powerup
        self.powerup = None

        # font
        self.font = pygame.font.SysFont('Comic Sans MS', 80)

    # create a new game
    def new(self):
        # start playing
        self.playing = True

        # create sprite groups
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.players = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.player_bullets = pygame.sprite.LayeredUpdates()
        self.enemy_bullets = pygame.sprite.LayeredUpdates()
        self.planets = pygame.sprite.LayeredUpdates()

        self.player = Player(self)

    # event handling
    def events(self):
        for event in pygame.event.get():  # check through each event
            if event.type == pygame.QUIT:  # if user pressed 'X' button
                # exit the loop
                self.playing = False
                self.running = False

    # update game
    def update(self):
        self.all_sprites.update()

    # draw stuff
    def draw(self):
        # fill screen
        self.screen.fill(black)

        # draw all sprites on the screen
        self.all_sprites.draw(self.screen)

        # make sure everything is running at a constant fps
        self.clock.tick(fps)

        # draw all bars
        self.player.draw_shoot_bar()
        self.player.draw_health_bar()
        self.player.draw_planet_bar()

        for enemy in self.enemies:
            enemy.draw_health_bar()

        # draw arrow
        self.player.draw_arrow()

        # draw quid
        self.player.draw_quid()

        # draw kills
        self.player.draw_kills()

        # draw the powerup icons
        icons = [
            'damage',
            'firerate',
            'heal',
            'healtime',
            'killheal',
            'maxhealth',
            'planet',
            'quid',
            'speed'
        ]
        for i in range(9):
            path = f'img/powerups/{icons[i]}.png'
            PowerupIcon(self, i * width / 9, height - 110, path)

        # update the screen
        pygame.display.update()

    # main game loop
    def main(self):
        while self.playing:
            self.player.events()
            self.update()
            self.draw()

    # intro screen
    def intro_screen(self):
        intro = True

        intro_title = self.font.render('Runaway', True, light_grey)
        intro_title_rect = intro_title.get_rect(center=(width / 2, 80))
        play_button = Button(width / 2, height / 2, 200, 60, light_grey, darker_grey, 'Play', 32)
        
        background = pygame.image.load('img/backgrounds/space_background.png')

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            self.screen.blit(background, (0, 0))
            self.screen.blit(intro_title, intro_title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            pygame.display.update()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

    # game over screen
    def game_over(self):
        text = self.font.render('Game Over', True, red)
        text_rect = text.get_rect(center=(width / 2, 80))

        restart_button = Button(width / 2, height / 2, 200, 60, light_grey, darker_grey, 'Restart', 32)
        background = pygame.image.load('img/backgrounds/space_background.png')

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            self.screen.blit(background, (0, 0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            pygame.display.update()

    # backstory
    def backstory(self):
        background = pygame.image.load('img/backstory.png')
        next_button = Button(width - (170 / 2) - 9, height - (50 / 2) - 10, 170, 50, white, green, 'Skip', 24)

        is_running = True
        while is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if next_button.is_pressed(mouse_pos, mouse_pressed):
                is_running = False

            self.screen.blit(background, (0, 0))
            self.screen.blit(next_button.image, next_button.rect)
            pygame.display.update()

# check if the file is being run and not imported
if __name__ == '__main__':
    # create an instance of the game
    g = Game()

    # show the intro screen
    g.intro_screen()

    # show the backstory
    g.backstory()

    # prepare the game
    g.new()

    # main loop
    while g.running:
        g.main()

        # once game is done show the game over screen
        g.game_over()

    # exit out of pygame and quit the program
    pygame.quit()
    sys.exit()

