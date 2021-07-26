import sys
from time import sleep
from random import randint
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from star import Star


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры"""

    def __init__(self):
        """Инициализирует игру и задает игровые ресурсы"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.screen = pygame.display.set_mode((1280, 800))
        self.settings.screen_height = self.screen.get_rect().height
        self.settings.screen_widht = self.screen.get_rect().width
        # Создание фона для игры
        self.stars = pygame.sprite.Group()
        self._create_mas_of_stars()
        self.screen.fill(self.settings.bg_color)
        self.stars.draw(self.screen)
        pygame.display.flip()
        self.screenshot = self.screen.copy()

        pygame.display.set_caption("Alien Invasion")
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, 'Play')
        self.bullets_speed_button = Button(self,
                                           f'Bullets speed: {self.settings.bullet_speed_factor}',
                                           26, 60)
        self.aliens_speed_button = Button(self,
                                          f'Aliens speed: {self.settings.alien_speed_factor}',
                                          26, 120)
        self.ship_speed_button = Button(self,
                                        f'Ship speed: {self.settings.ship_speed_factor}',
                                        26, 180)
        self.reset_settings_button = Button(self, 'Reset settings', 36, 240)
        self.sb = Scoreboard(self)

    def _create_mas_of_stars(self):
        """Создает массив звезд с заданным разряжением"""
        star = Star(self)
        self.stars.add(star)
        num_of_column = self.settings.screen_widht // (
                self.settings.star_rarefaction * 2) + 1
        num_of_rows = self.settings.screen_height // (
                self.settings.star_rarefaction * 2) + 1
        for row_num in range(num_of_rows):
            for col_num in range(num_of_column):
                self._create_star(col_num, row_num)

    def _create_star(self, col_num, row_num):
        """Создает экземпляр звезды, задает координаты и добавляет в массив"""
        star = Star(self)
        star.rect.x = self.settings.star_rarefaction + 2 * \
                      self.settings.star_rarefaction * col_num + \
                      randint(-self.settings.star_rarefaction // 2,
                              self.settings.star_rarefaction // 2)
        star.rect.y = self.settings.star_rarefaction + 2 * \
                      self.settings.star_rarefaction * row_num + \
                      randint(-self.settings.star_rarefaction,
                              self.settings.star_rarefaction)
        self.stars.add(star)

    def _check_events(self):
        """Отслеживание событий клавиатуры и мыши"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._exit_game()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
                if event.key == pygame.K_ESCAPE:
                    self._exit_game()
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.detect_button_clicked(mouse_pos)

    def _exit_game(self):
        """Обновляет рекорд и закрывает игру """
        self.sb.set_high_score()
        sys.exit()

    def detect_button_clicked(self, mouse_pos):
        """Передает позицию мыши методам кнопок"""
        if not self.stats.game_active:
            self._check_play_button(mouse_pos)
            self._check_bullet_speed_button(mouse_pos)
            self._check_ship_speed_button(mouse_pos)
            self._check_alien_speed_button(mouse_pos)
            self._check_reset_settings(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """запускает новую игру при нажатии кнопки 'Play'"""
        button_play_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_play_clicked:
            self.start_game()

    def _check_bullet_speed_button(self, mouse_pos):
        """Меняет настройки скорости полета пули при нажатии на кнопку"""
        button_bullet_speed_clicked = self.bullets_speed_button.rect.collidepoint(
            mouse_pos)
        if button_bullet_speed_clicked and self.settings.bullet_speed_factor < \
                self.settings.bullet_speed_limit:
            self.settings.bullet_speed_factor *= self.settings.speedup_scale

    def _check_alien_speed_button(self, mouse_pos):
        """Меняет настройки скорости полета пули при нажатии на кнопку"""
        button_alien_speed_clicked = self.aliens_speed_button.rect.collidepoint(
            mouse_pos)
        if button_alien_speed_clicked:
            self.settings.alien_speed_factor *= self.settings.speedup_scale

    def _check_ship_speed_button(self, mouse_pos):
        """Меняет настройки скорости полета пули при нажатии на кнопку"""
        button_ship_speed_clicked = self.ship_speed_button.rect.collidepoint(
            mouse_pos)
        if button_ship_speed_clicked and self.settings.ship_speed_factor < \
                self.settings.ship_speed_limit:
            self.settings.ship_speed_factor *= self.settings.speedup_scale

    def _check_reset_settings(self, mouse_pos):
        """Сбрасывает статистику"""
        button_reset_settings_clicked = self.reset_settings_button.rect.collidepoint(
            mouse_pos)
        if button_reset_settings_clicked:
            self.settings.initialize_dynamic_settings()

    def start_game(self):
        """Стартует игру"""
        # Сброс игровой статистики
        self.stats.reset_stats()
        self.sb.prep_score()
        self.stats.game_active = True
        # Очистка списков пришельцев и снарядов
        self.aliens.empty()
        self.bullets.empty()
        # Создание нового флота и размещение корабля в центре
        self._create_fleet()
        self.ship.center_ship()

        # Убираем указатель мымши
        pygame.mouse.set_visible(False)

    def pause_game(self):
        """Ставит игру на паузу"""
        if not self.stats.game_pause:
            self.stats.game_pause = True
        else:
            self.stats.game_pause = False

    def _check_keydown_events(self, event):
        """Реагирует на нажатие кклавиш"""
        if event.key == pygame.K_RIGHT and self.stats.game_active:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT and self.stats.game_active:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE and self.stats.game_active:
            self._fire_bullet()
        elif event.key == pygame.K_SPACE and not self.stats.game_active:
            self.start_game()
        elif event.key == pygame.K_PAUSE:
            self.pause_game()

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
        colissions = pygame.sprite.groupcollide(self.bullets, self.aliens, True,
                                                True)
        if colissions:
            for aliens in colissions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            # удаление снарядов и создание флота
            self.bullets.empty()
            self._create_fleet()
            # повышение скорости игры
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

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
            self.sb.prep_ships()
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
            self.settings.initialize_dynamic_settings()
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Реагирует на достижение пришельцами низа экрана"""
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
        # self.screen.fill(self.settings.bg_color)
        # self.stars.draw(self.screen)
        self.screen.blit(self.screenshot, (0, 0))
        # Прорисовка корабля
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        if not self.stats.game_active:
            self._draw_buttons()
        self.sb.show_score()
        # Отображение последнего прорисованного экрана
        pygame.display.flip()

    def _draw_buttons(self):
        """Рисует кнопки"""
        self.play_button.draw_button()
        self.bullets_speed_button.dinamic_msg_draw(
            f'Bullets speed: {int(self.settings.bullet_speed_factor * 10)}')
        self.aliens_speed_button.dinamic_msg_draw(
            f'Aliens speed: {int(self.settings.alien_speed_factor * 10)}')
        self.ship_speed_button.dinamic_msg_draw(
            f'Ship speed: {int(self.settings.ship_speed_factor * 10)}')
        self.reset_settings_button.draw_button()

    def run_game(self):
        """Запуск основного цикла игры"""
        while True:
            self._check_events()
            if self.stats.game_active and not self.stats.game_pause:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()


if __name__ == '__main__':
    """Создание экземпляра и запуск игры"""
    ai = AlienInvasion()
    ai.run_game()
