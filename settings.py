class Settings:
    """Класс для хранения настроек игры Alien Invasion"""

    def __init__(self):
        """Инициализирует настройки игры"""
        """Параметры экрана"""
        self.screen_widht = 1000
        self.screen_height = 500
        """Назначение цвета фона"""
        self.bg_color = 230, 230, 230
        self.ship_speed = 0.5

