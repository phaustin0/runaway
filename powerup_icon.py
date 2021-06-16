# poweup icon class file
import pygame


class PowerupIcon:
    def __init__(self, game, x, y, path):
        self.game = game

        self.x = x
        self.y = y

        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.game.screen.blit(self.image, self.rect)

