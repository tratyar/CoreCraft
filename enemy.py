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
        global bos
        if self.enemy_image == 'boss.png':
            bos = 1
        else:
            bos = 0
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
        bullet = Bullet(self.rect.centerx, self.rect.bottom)
        self.bullets.add(bullet)


class T_0(Enemy):
    enemy_image = "T_0.png"
    base_speed = 2
    base_shoot_delay = 1200


class T_1(Enemy):
    enemy_image = "T_1.png"
    base_speed = 1
    base_shoot_delay = 1000


class T_2(Enemy):
    enemy_image = "T_2.png"
    base_speed = 2
    base_shoot_delay = 800


class T_3(Enemy):
    enemy_image = "T_3.png"
    base_speed = 1
    base_shoot_delay = 600


class boss(Enemy):
    enemy_image = "boss.png"
    base_speed = 2
    base_shoot_delay = 300


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        if bos == 1:
            self.rect.centerx = x + random.choice([-100, 100])
            self.rect.bottom = y
        else:
            self.rect.centerx = x
            self.rect.bottom = y
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 900:
            self.kill()