import pygame.font


class Button:
    def __init__(self, ai_game, msg, font_size=48, deviation_y=0):
        self.screen = ai_game.screen
        self.deviation_y = deviation_y
        self.screen_rect = self.screen.get_rect()

        # Назаначение атрибутов и свойств кнопки
        self.widht, self.height = 200, 50
        self.button_color = (0, 0, 255)
        self.text_color = (255, 255, 255)
        self.font_size = font_size
        self.font = pygame.font.SysFont(None, self.font_size)

        # построение  объекта rect кнопки и выравнивание по центру экрана
        self.rect = pygame.Rect(0, 0, self.widht, self.height)
        self.rect.center = self.screen_rect.center
        self.rect.y += self.deviation_y

        # Сообщение кнопки создается только один раз
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Преобразует msg в прямоугольник и выравнивает текст по центру"""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        # self.msg_image_rect.y += self.deviation

    def draw_button(self):
        """Рисует статичные кнопки"""
        # Отображение пустой кнопки и вывод сообщения
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def dinamic_msg_draw(self, msg):
        """Рисует кнопки с изменяемым содержимым"""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
