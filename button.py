# button class file
import pygame


class Button:
    def __init__(self, x, y, width, height, text_colour, bg_colour, text, font_size):
        self.font = pygame.font.SysFont('Comic Sans MS', font_size)
        self.text = text

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.text_colour = text_colour
        self.bg_colour = bg_colour

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.bg_colour)
        self.rect = self.image.get_rect()

        self.rect.centerx = self.x
        self.rect.centery = self.y

        self.text = self.font.render(self.text, True, self.text_colour)
        self.text_rect = self.text.get_rect(center=(self.width / 2, self.height / 2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pos, pressed):
        if self.rect.collidepoint(pos):
            return True if pressed[0] else False
        return False

