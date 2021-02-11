class Settings:
    """Класс для хранения настроек игры Alien Invasion"""

    def __init__(self):
        """Инициализирует настройки игры"""
        """Параметры экрана"""
        self.screen_widht = 1000
        self.screen_height = 500
        """Назначение цвета фона"""
        self.bg_color = 230, 230, 230
        # скорость движения корабля
        self.ship_speed = 1
        # Параетры снаряда
        self.bullet_speed = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 230, 60, 60
        self.bullet_allowed = 3
        self.alien_speed = 0.2
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
