import math

import pygame
import sys
import os


def load_image(name, colorkey=None):
    fullname = os.path.join('media\\sprite', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def batl_im(im, colorkey=None):
    image = pygame.transform.scale(im, (15, 15))
    return image


class Core(pygame.sprite.Sprite): #ядро
    def __init__(self, y, x, *group, args=''):
        super().__init__(*group)
        self.lvl = int(args[0])
        self.xp = int(args[1])
        self.defens = int(args[2])
        self.attack = int(args[3])
        self.vip = int(args[4])
        self.image = load_image('blocks\\' + args[5])
        self.batl_im = batl_im(self.image)
        self.up = int(args[6])
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.x = x - 5
        self.y = y - 5

    def revers_mod(self):
        self.image, self.batl_im = self.batl_im, self.image

    def update(self, *args):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0] + self.x * 15
        self.rect.y = pos[1] + self.y * 15


class Machine_gun(pygame.sprite.Sprite): #пулемёт
    def __init__(self, y, x, *group, args=''):
        super().__init__(*group)
        self.lvl = int(args[0])
        self.bull_sp = int(args[2])
        self.dmg = int(args[3])
        self.shots_in_shot = int(args[4])
        self.image = load_image('blocks\\' + args[5])
        self.batl_im = batl_im(self.image)
        self.sell = int(args[6])
        self.buy = int(args[7])
        self.up = int(args[8])
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.x = x - 5
        self.y = y - 5
        # выстрелы
        self.bullets = pygame.sprite.Group()
        self.last_shot = pygame.time.get_ticks()
        self.at_sp = float(args[1])

    def revers_mod(self):
        self.image, self.batl_im = self.batl_im, self.image

    def update(self, *args):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0] + self.x * 15
        self.rect.y = pos[1] + self.y * 15
        # стрельба
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.at_sp * 500:
            self.last_shot = now
            self.shoot()

        self.bullets.update()
        self.bullets.draw(pygame.display.get_surface())

    def shoot(self):
        if self.shots_in_shot == 1:
            bullet = Bullet_min_gun(self.rect.x + 7, self.rect.bottom - 10, self.bull_sp, self.dmg)
            self.bullets.add(bullet)
        elif self.shots_in_shot == 2:
            bullet = Bullet_min_gun(self.rect.x + 5, self.rect.bottom - 10, self.bull_sp, self.dmg)
            self.bullets.add(bullet)
            bullet = Bullet_min_gun(self.rect.x + 10, self.rect.bottom - 10, self.bull_sp, self.dmg)
            self.bullets.add(bullet)
        elif self.shots_in_shot == 3:
            bullet = Bullet_min_gun(self.rect.x + 3, self.rect.bottom - 10, self.bull_sp, self.dmg)
            self.bullets.add(bullet)
            bullet = Bullet_min_gun(self.rect.x + 8, self.rect.bottom - 10, self.bull_sp, self.dmg)
            self.bullets.add(bullet)
            bullet = Bullet_min_gun(self.rect.x + 13, self.rect.bottom - 10, self.bull_sp, self.dmg)
            self.bullets.add(bullet)


class Bullet_min_gun(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, dmg):
        super().__init__()
        s = pygame.Surface((4, 20), pygame.SRCALPHA)
        pygame.draw.rect(s, (46, 222, 27), (0, 0, 4, 5), 0)
        pygame.draw.rect(s, (46, 222, 27, 204), (0, 6, 4, 10), 0)
        pygame.draw.rect(s, (46, 222, 27, 153), (0, 11, 4, 15), 0)
        pygame.draw.rect(s, (46, 222, 27, 102), (0, 16, 4, 20), 0)
        self.image = s
        self.dmg = dmg
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = speed

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -10:
            self.kill()


class Armor(pygame.sprite.Sprite): #броня
    def __init__(self, y, x, *group, args=''):
        super().__init__(*group)
        self.lvl = int(args[0])
        self.xp = int(args[1])
        self.image = load_image('blocks\\' + args[2])
        self.batl_im = batl_im(self.image)
        self.sell = int(args[3])
        self.buy = int(args[4])
        self.up = int(args[5])
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.x = x - 5
        self.y = y - 5

    def revers_mod(self):
        self.image, self.batl_im = self.batl_im, self.image

    def update(self, *args):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0] + self.x * 15
        self.rect.y = pos[1] + self.y * 15


class Shot_gun(pygame.sprite.Sprite):
    def __init__(self, y, x, *group, args=''):
        super().__init__(*group)
        self.lvl = int(args[0])
        self.bull_sp = int(args[2])
        self.dmg = int(args[3])
        self.shots_in_shot = int(args[4])
        self.image = load_image('blocks\\' + args[5])
        self.batl_im = batl_im(self.image)
        self.sell = int(args[6])
        self.buy = int(args[7])
        self.up = int(args[8])
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.x = x - 5
        self.y = y - 5
        # выстрелы
        self.bullets = pygame.sprite.Group()
        self.last_shot = pygame.time.get_ticks()
        self.at_sp = float(args[1])

    def revers_mod(self):
        self.image, self.batl_im = self.batl_im, self.image

    def update(self, *args):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0] + self.x * 15
        self.rect.y = pos[1] + self.y * 15
        # стрельба
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.at_sp * 500:
            self.last_shot = now
            self.shoot()

        self.bullets.update()
        self.bullets.draw(pygame.display.get_surface())

    def shoot(self):
        bullet = Bullet_shot_gun(self.rect.x + 7, self.rect.bottom - 10, self.bull_sp, 0, self.dmg)
        self.bullets.add(bullet)
        for i in range(1, self.shots_in_shot // 2 + 1):
            bullet = Bullet_shot_gun(self.rect.x + 7, self.rect.bottom - 10, self.bull_sp, i, self.dmg)
            self.bullets.add(bullet)
            bullet = Bullet_shot_gun(self.rect.x + 7, self.rect.bottom - 10, self.bull_sp, -i, self.dmg)
            self.bullets.add(bullet)



class Bullet_shot_gun(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, angl, dmg):
        super().__init__()
        s = pygame.Surface((4, 20), pygame.SRCALPHA)
        pygame.draw.rect(s, (34, 177, 76), (0, 0, 4, 5), 0)
        pygame.draw.rect(s, (34, 177, 76, 204), (0, 6, 4, 10), 0)
        pygame.draw.rect(s, (34, 177, 76, 153), (0, 11, 4, 15), 0)
        pygame.draw.rect(s, (34, 177, 76, 102), (0, 16, 4, 20), 0)
        self.dmg = dmg
        self.image = s
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = speed
        self.angl = angl

    def update(self):
        self.rect.x += self.angl
        self.rect.y -= self.speed
        if self.rect.y < -10:
            self.kill()


class Test: #класс для определения типа модуля
    def __init__(self):
        self.moduls = pygame.sprite.Group()

    def testing(self, data, y, x):
        if data[0] == 'core':
            return Core(y, x, self.moduls, args=data[1:])
        if data[0] == 'armor':
            return Armor(y, x, self.moduls, args=data[1:])
        if data[0] == 'machine_gun':
            return Machine_gun(y, x, self.moduls, args=data[1:])
        if data[0] == 'shot_gun':
            return Shot_gun(y, x, self.moduls, args=data[1:])


