import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Класс, представляющий пришельца"""

    def __init__(self, ai_game):
        """Инициализирует пришельца и задает его начальную позицию"""
        super().__init__()
        self.screen = ai_game.screen

        # загрузка изображения пришшельца и назначение атрибута rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Каждый глвые пришелец появляется в верхнем левом углу экрана?
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохраняем координату х пришельца в вещественном виде в атрибуте х
        self.x = float(self.rect.x)
        self.settings = ai_game.settings

    def update(self):
        """Перемещает пришельца вправо"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True


