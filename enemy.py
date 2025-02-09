import pygame
import random
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('media\\sprite\\ship', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Enemy(pygame.sprite.Sprite):
    def __init__(self, *group, index=0, total_enemies=1, level=1, max_health=300):
        super().__init__(*group)
        self.image = load_image(self.enemy_image, -1)
        self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.image.get_rect()

        # Рассчитываем позицию врага
        screen_width = 1200
        spacing = screen_width // (total_enemies + 1)
        self.rect.x = spacing * (index + 1) - self.rect.width // 2
        self.rect.y = random.randint(40, 150)  # Начальная позиция в пределах верхней части экрана

        self.speed = self.base_speed
        self.shoot_delay = self.base_shoot_delay

        self.lvl = level
        self.bullets = pygame.sprite.Group()
        self.last_shot = pygame.time.get_ticks()

        # Начальные параметры для движения
        self.horizontal_speed = random.choice([-self.speed, self.speed])  # скорость влево-вправо
        self.vertical_speed = self.speed  # скорость вверх или вниз

        # Здоровье врага
        self.max_health = max_health  # Максимальное здоровье
        self.health = self.max_health  # Текущее здоровье

    def update(self, player_rect):
        # Движение врага
        self.rect.x += self.horizontal_speed
        self.rect.y += self.vertical_speed

        # Проверка границ экрана
        if self.rect.x < 0 or self.rect.x > 1200 - self.rect.width:
            self.horizontal_speed = -self.horizontal_speed  # Изменяем направление при касании границы

        if self.rect.y < 40 or self.rect.y > 150:
            self.vertical_speed = -self.vertical_speed  # Изменяем направление при достижении верхнего или нижнего предела

        # Стрельба по игроку
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.shoot(player_rect)

        self.bullets.update()
        self.bullets.draw(pygame.display.get_surface())

        # Отрисовка полоски здоровья
        self.draw_health_bar()

    def take_damage(self, amount):
        self.health -= amount  # Уменьшаем здоровье
        if self.health <= 0:  # Если здоровье меньше или равно 0
            self.kill()  # Уничтожаем врага

    def draw_health_bar(self):
        # Размеры полоски здоровья
        bar_width = self.rect.width
        bar_height = 5
        fill = (self.health / self.max_health) * bar_width  # Заполненная часть полоски

        # Позиция полоски здоровья (над врагом)
        bar_x = self.rect.x
        bar_y = self.rect.y - 10

        # Отрисовка фона полоски здоровья (красный)
        pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        # Отрисовка заполненной части полоски здоровья (зеленый)
        pygame.draw.rect(pygame.display.get_surface(), (0, 255, 0), (bar_x, bar_y, fill, bar_height))

    def shoot(self, player_rect):
        # Создаем пули в указанных точках спавна
        for offset in self.bullet_spawn_offsets:
            bullet = Bullet(self.rect.centerx + offset[0], self.rect.bottom + offset[1])
            self.bullets.add(bullet)


class T_0(Enemy):
    enemy_image = "T_0.png"
    base_speed = 2
    base_shoot_delay = 1200
    bullet_spawn_offsets = [(0, 0)]  # Одна точка спавна пуль


class T_1(Enemy):
    enemy_image = "T_1.png"
    base_speed = 1
    base_shoot_delay = 1000
    bullet_spawn_offsets = [(-25, -20), (25, -20)]  # Две точки спавна пуль


class T_2(Enemy):
    enemy_image = "T_2.png"
    base_speed = 2
    base_shoot_delay = 900
    bullet_spawn_offsets = [(-20, -60), (20, -60)]  # Две точки спавна пуль


class T_3(Enemy):
    enemy_image = "T_3.png"
    base_speed = 1
    base_shoot_delay = 800
    bullet_spawn_offsets = [(-22, -80), (22, -80)]  # Две точки спавна пуль


class boss(Enemy):
    enemy_image = "boss.png"
    base_speed = 2
    base_shoot_delay = 700  # Задержка для обычных снарядов
    bullet_spawn_offsets = [(-90, -40), (90, -40), (-70, -30), (70, -30), (-75, -30), (75, -30),
                            (-150, 0), (150, 0), (200, -50), (-200, -50), (95, -40), (-95, -40),   # Точки спавна пуль красные
                            (-48, -35), (-160, 0), (160, 0), (48, -35), (-55, -35), (55, -35), (-40, -35), (40, -35), (120, 0), (-120, 0),
                            (-78, -35), (78, -35), (-68, -35), (68, -35)]   # Точки спавна пуль ракет

    def __init__(self, *group, index=0, total_enemies=1, level=1, max_health=5000):
        super().__init__(*group, index=index, total_enemies=total_enemies, level=level, max_health=max_health)
        self.blue_bullets = pygame.sprite.Group()  # Группа для синих снарядов
        self.last_shot = pygame.time.get_ticks()
        self.last_shot1 = pygame.time.get_ticks()# Время последнего выстрела
        self.shoot_delay = 1500  # Задержка между выстрелами (1.5 секунды)
        self.shoot_delay1 = 900

    def update(self, player_rect):
        super().update(player_rect)  # Вызываем родительский метод для обычной логики
        # Стрельба
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.shoot(player_rect)

        if now - self.last_shot1 > self.shoot_delay1:
            self.last_shot1 = now
            self.shoot1(player_rect)

        self.blue_bullets.update()
        self.blue_bullets.draw(pygame.display.get_surface())

    def shoot(self, player_rect):
        # Создаем 14 красных пуль
        for offset in self.bullet_spawn_offsets[:14]:  # Первые шесть точек для красных пуль
            bullet = Bullet(self.rect.centerx + offset[0], self.rect.bottom + offset[1])
            self.bullets.add(bullet)

        # Создаем 8 синих пули
        for offset in self.bullet_spawn_offsets[14:]:  # Последние четыре точки для синих пуль
            blue_bullet = BlueBullet(self.rect.centerx + offset[0], self.rect.bottom + offset[1])
            self.blue_bullets.add(blue_bullet)

    def shoot1(self, player_rect):
        for offset in self.bullet_spawn_offsets[:14]:  # Первые шесть точек для красных пуль
            bullet = Bullet(self.rect.centerx + offset[0], self.rect.bottom + offset[1])
            self.bullets.add(bullet)




class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 10))
        self.image.fill((255, 0, 0))  # Красный цвет
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 900:
            self.kill()


class BlueBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((6, 12))  # Синий снаряд больше и толще
        self.image.fill((0, 0, 255))  # Синий цвет
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 3  # Медленнее обычных снарядов
        self.damage = 2  # Наносит 2 HP урона

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 900:
            self.kill()