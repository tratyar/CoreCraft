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


class Core(pygame.sprite.Sprite): #ядро
    def __init__(self, *group, args=''):
        super().__init__(*group)
        self.lvl = int(args[0])
        self.xp = int(args[1])
        self.defens = int(args[2])
        self.attack = int(args[3])
        self.vip = int(args[4])
        self.image = load_image('blocks\\' + args[5])
        self.up = int(args[6])
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class Machine_gun(pygame.sprite.Sprite): #пулемёт
    def __init__(self, *group, args=''):
        super().__init__(*group)
        self.lvl = int(args[0])
        self.at_sp = int(args[1])
        self.bull_sp = int(args[2])
        self.dmg = int(args[3])
        self.shot = int(args[4])
        self.image = load_image('blocks\\' + args[5])
        self.sell = int(args[6])
        self.buy = int(args[7])
        self.up = int(args[8])
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class Armor(pygame.sprite.Sprite): #броня
    def __init__(self, *group, args=''):
        super().__init__(*group)
        self.lvl = int(args[0])
        self.xp = int(args[1])
        self.image = load_image('blocks\\' + args[2])
        self.sell = int(args[3])
        self.buy = int(args[4])
        self.up = int(args[5])
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0


class Test: #класс для определения типа модуля
    def __init__(self):
        self.moduls = pygame.sprite.Group()

    def testing(self, data):
        if data[0] == 'core':
            return Core(self.moduls, args=data[1:])
        if data[0] == 'armor':
            return Armor(self.moduls, args=data[1:])
        if data[0] == 'machine_gun':
            return Machine_gun(self.moduls, args=data[1:])


