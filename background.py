# background class file
import pygame
from settings import *

# background settings
bg_layer = 1


class Background(pygame.sprite.Sprite):
    def __init__(self, game, path):
        self.game = game
        self._layer = bg_layer

        # add to the relevant groups
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        # create the images
        bg_img_0 = pygame.image.load(path)
        bg_img_1 = pygame.image.load(path)
        bg_img_2 = pygame.image.load(path)
        bg_img_3 = pygame.image.load(path)
        bg_img_4 = pygame.image.load(path)
        bg_img_5 = pygame.image.load(path)
        bg_img_6 = pygame.image.load(path)
        bg_img_7 = pygame.image.load(path)
        bg_img_8 = pygame.image.load(path)
        self.image = pygame.Surface([3 * width, 3 * height])
        self.image.blit(bg_img_0, (0, 0, width, height))
        self.image.blit(bg_img_1, (width, 0, width, height))
        self.image.blit(bg_img_2, (2 * width, 0, width, height))
        self.image.blit(bg_img_3, (0, height, width, height))
        self.image.blit(bg_img_4, (width, height, width, height))
        self.image.blit(bg_img_5, (2 * width, height, width, height))
        self.image.blit(bg_img_6, (0, 2 * height, width, height))
        self.image.blit(bg_img_7, (width, 2 * height, width, width))
        self.image.blit(bg_img_8, (2 * width, 2 * height, width, height))

        # get the rect of the background
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)

    # update the background
    def update(self):
        # reposition the background
        self.reposition()

    # repositioning background
    def reposition(self):
        if self.rect.top >= 0:
            self.rect.top = -height
        if self.rect.bottom <= height:
            self.rect.bottom = 2 * height
        if self.rect.left >= 0:
            self.rect.left = -width
        if self.rect.right <= width:
            self.rect.right = 2 * width

    # change the background
    def change_background(self, path):
        bg_img_0 = pygame.image.load(path)
        bg_img_1 = pygame.image.load(path)
        bg_img_2 = pygame.image.load(path)
        bg_img_3 = pygame.image.load(path)
        bg_img_4 = pygame.image.load(path)
        bg_img_5 = pygame.image.load(path)
        bg_img_6 = pygame.image.load(path)
        bg_img_7 = pygame.image.load(path)
        bg_img_8 = pygame.image.load(path)
        self.image.blit(bg_img_0, (0, 0, width, height))
        self.image.blit(bg_img_1, (width, 0, width, height))
        self.image.blit(bg_img_2, (2 * width, 0, width, height))
        self.image.blit(bg_img_3, (0, height, width, height))
        self.image.blit(bg_img_4, (width, height, width, height))
        self.image.blit(bg_img_5, (2 * width, height, width, height))
        self.image.blit(bg_img_6, (0, 2 * height, width, height))
        self.image.blit(bg_img_7, (width, 2 * height, width, width))
        self.image.blit(bg_img_8, (2 * width, 2 * height, width, height))

