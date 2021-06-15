# Main file to handle all game logic
import pygame
import sys
from settings import *
from player import *
from enemy import *
from planet import *


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
        Planet(self, 500, 500)
        Planet(self, 448, 566)
        Planet(self, 537, 525)
        Planet(self, 389, 33)

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

        # update the screen
        pygame.display.update()

    # main game loop
    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

    # intro screen TODO
    def intro_screen(self):
        pass

    # game over screen TODO
    def game_over(self):
        pass

# check if the file is being run and not imported
if __name__ == '__main__':
    # create an instance of the game
    g = Game()

    # show the intro screen
    g.intro_screen()

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

