import pygame
from pygame.sprite import Sprite
from random import randint



class Star(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        x = randint(1, 550)
        if x == 1:
            self.image = pygame.image.load('images/star1.png')
        elif x % 10 == 2 and x % 100 == 2:
            self.image = pygame.image.load('images/star2.png')
        elif x % 10 == 3:
            self.image = pygame.image.load('images/star3.png')
        elif x == 4:
            self.image = pygame.image.load('images/star4.png')
        elif x == 5 or x == 105:
            self.image = pygame.image.load('images/star5.png')
        elif x % 10 == 6:
            self.image = pygame.image.load('images/star6.png')
        elif x == 7:
            self.image = pygame.image.load('images/star7.png')
        elif x == 8 or x == 108:
            self.image = pygame.image.load('images/star8.png')
        else:
            self.image = pygame.image.load('images/star9.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
