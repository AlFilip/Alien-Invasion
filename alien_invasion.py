import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры"""

    def __init__(self):
        """Инициализирует игру и задает игровые ресурсы"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_height = self.screen.get_rect().height
        self.settings.screen_widht = self.screen.get_rect().width
        pygame.display.set_caption("Alien Invasion")
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def _check_events(self):
        """Отслеживание событий клавиатуры и мыши"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Реагирует на нажатие кклавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Создание нового снаряда и вклбчение его в группу bullets"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Обновляет снаряды и Удаляет пули, вышедшие за край экрана"""
        # перемещает снаряды вверх по экрану
        self.bullets.update()
        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self):
        """Обработка коллизий снарядов с пришельцами"""
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens,
                                                False,
                                                True)
        if not self.aliens:
            # удаление снарядов и создание флота
            self.bullets.empty()
            self._create_fleet()

    def _create_fleet(self):
        """Создание флота вторжения"""
        # создание пришельца и добавление его во флот
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        self.aliens.add(alien)
        available_space_x = self.settings.screen_widht - 2 * alien_width
        number_aliens_x = available_space_x // (2 * alien_width)
        self.ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - 3 * alien_height - \
                            self.ship_height
        number_raws = available_space_y // (2 * alien_height)
        for row_number in range(number_raws):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Создание пришельца"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        """Управляет движением флота"""
        self._check_fleet_edges()
        self.aliens.update()
        # Проверка столкновений пришелец - корабль
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def _ship_hit(self):
        """реакция на столкновение корабля игрока и пришельцев"""
        # -1 жизнь
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            # очитска поля от пришельцев и снарядов
            self.bullets.empty()
            self.aliens.empty()
            # создание нового флота и центровка корабля
            self._create_fleet()
            self.ship.center_ship()
            # пауза
            sleep(0.5)
        else:
            self.stats.game_active = False

    def _check_aliens_bottom(self):
        scren_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= scren_rect.bottom:
                self._ship_hit()
                break

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """опускает флот вниз и меняет направление его движения"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Обновляет экран и изображения на нем"""
        # Заливка фона экрана назначенным фоновым цветом
        self.screen.fill(self.settings.bg_color)
        # Прорисовка корабля
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        # Отображение последнего прорисованного экрана
        pygame.display.flip()

    def run_game(self):
        """Запуск основного цикла игры"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()


if __name__ == '__main__':
    """Создание экземпляра и запуск игры"""
    ai = AlienInvasion()
    ai.run_game()
