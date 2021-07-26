class Settings:
    """Класс для хранения настроек игры Alien Invasion"""

    def __init__(self):
        """Инициализирует настройки игры"""
        #Параметры экрана
        self.screen_widht = 1000
        self.screen_height = 500
        #Назначение цвета фона
        self.bg_color = 0, 0, 0
        # скорость движения корабля
        # self.ship_speed = 1
        # Параетры снаряда
        # self.bullet_speed = 1.5
        self.bullet_width = 4
        self.bullet_height = 15
        self.bullet_color = 255, 0, 0
        self.bullet_allowed = 3
        self.bullet_speed_limit = 20
        # self.alien_speed = 0.2
        self.fleet_drop_speed = 20
        self.fleet_direction = 1
        self.ship_limit = 3
        self.ship_speed_limit = 5
        self.speedup_scale = 1.2
        self.score_scale = 1.5
        self.star_rarefaction = 30
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициирует изменяемые в процессе игры настройк"""
        self.ship_speed_factor = 1
        self.bullet_speed_factor = 1.5
        self.alien_speed_factor = 1

        # 1 вправо, -1 влево
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        """Увеличивает настроййки скорости"""
        if self.ship_speed_factor < self.ship_speed_limit:
            self.ship_speed_factor *= self.speedup_scale
        if self.bullet_speed_factor < self.bullet_speed_limit:
            self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
