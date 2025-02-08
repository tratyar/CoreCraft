import os
import sys
import pygame
from blocks import *
from my_ship import *
import random
pygame.init()


board = None
move = None
buy = False
cache = 0


def save_info():
    with open('saves.txt', 'r') as f:
        data = f.readlines()
        data = list(map(str.rstrip, data))
    data[1] = cache
    with open('saves.txt', 'w') as f:
        f.write('\n'.join(list(map(str, data))))


class Board: #класс доскки
    def __init__(self):
        self.board = [[0 for _ in range(11)]for _ in range(11)]
        self.width = 11
        self.height = 11
        self.left = 20
        self.top = 20
        self.cell_size = 60
        self.color = [(100, 100, 100)]
        self.test = Test()
        self.load_bord()

    def load_bord(self): #подстановка классов в поле
        global board, move
        if not board:
            self.board = [[0 for _ in range(11)] for _ in range(11)]
            data = list(open('data.txt', encoding='utf8', mode='r'))
            tabl = list(open('saves.txt', encoding='utf8', mode='r'))[0][:-7].split(', ')
            for y in range(11):
                for x in range(11):
                    if tabl[x + y * 11] != '0':
                        for el in data:
                            if tabl[x + y * 11] in el:
                                el = el[15:].split()
                                self.board[y][x] = self.test.testing(el, y, x)
                                break
            for y in range(11):
                for x in range(11):
                    if type(self.board[y][x]) != int:
                        self.board[y][x].rect.x = 20 + x * 60
                        self.board[y][x].rect.y = 20 + y * 60
        else:
            self.board = board.copy()
            for y in range(11):
                for x in range(11):
                    if self.board[y][x] == 1:
                        self.board[y][x] = 0
                    if type(self.board[y][x]) == str:
                        data = list(open('data.txt', encoding='utf8', mode='r'))
                        for el in data:
                            if self.board[y][x] in el:
                                el = el[15:].split()
                                self.board[y][x] = self.test.testing(el, y, x)
                                break
            for y in range(11):
                for x in range(11):
                    if type(self.board[y][x]) != int:
                        self.board[y][x].rect.x = 20 + x * 60
                        self.board[y][x].rect.y = 20 + y * 60
                        if type(self.board[min(y, 9) + 1][x]) == int:
                            self.board[min(y, 9) + 1][x] = 1
                        if type(self.board[max(y, 1) - 1][x]) == int:
                            self.board[max(y, 1) - 1][x] = 1
                        if type(self.board[y][min(x, 9) + 1]) == int:
                            self.board[y][min(x, 9) + 1] = 1
                        if type(self.board[y][max(x, 1) - 1]) == int:
                            self.board[y][max(x, 1) - 1] = 1
        board = self.board

    def render(self, screen): #прогрузка поля
        global move
        for y in range(self.height + 1):
            pygame.draw.line(screen, self.color[0], (self.left, self.top + y * self.cell_size),
                             (self.left + self.width * self.cell_size, self.top + y * self.cell_size), 1)
        for x in range(self.width + 1):
            pygame.draw.line(screen, self.color[0], (self.left + self.cell_size * x, self.top),
                             (self.left + self.cell_size * x, self.top + self.height * self.cell_size), 1)
        if move or buy:
            for y in range(11):
                for x in range(11):
                    if self.board[y][x] == 1:
                        pygame.draw.rect(screen, (200, 200, 200), (45 + x * 60, 45 + y * 60, 10, 10), 0) # клеточки для постоновки блока


class Shop:
    def __init__(self):
        global cache
        self.save = list(open('saves.txt', encoding='utf8', mode='r'))
        self.cashe = int(self.save[1])
        cache = self.cashe
        self.shop_item = Shop_item()
        self.mod = 1

    def update(self, screen, args): # остальная часть магазина
        global move, cache
        if args and args[0].type == pygame.MOUSEBUTTONUP:
            self.shop_item.duit = True
        self.mod = self.shop_item.add_botton(screen, self.mod, cache, args) # отрисовка кнопок и типов блоков
        self.update_item_store(screen) # отрисовка блоков в магазине
        self.shop_item.open_info(screen, self.mod, args) # открытие информации по блоку
        if self.shop_item.buy_mode:
            self.shop_item.buy(screen, args)
        if self.shop_item.sell_mode:
            self.shop_item.sell_block(screen, args)
        if self.shop_item.upgrade_mode:
            self.shop_item.upgrade(screen, args)
        if move:
            self.shop_item.move_moduls(screen, args)

    def update_item_store(self, screen):
        if self.mod == 1:
            self.shop_item.defense(screen)
        elif self.mod == 2:
            self.shop_item.attack(screen)
        elif self.mod == 3:
            self.shop_item.vip(screen)


class Shop_item:
    def __init__(self):
        # переменные
        self.timer = 0
        # броня
        self.Armor = load_image('blocks\\armor_0.png')
        self.rectArmor = self.Armor.get_rect()
        self.rectArmor.x = 1100
        self.rectArmor.y = 80
        # оружие
        self.Machine_gun = load_image('blocks\\machine_0.png')
        self.rectMachine_gun = self.Machine_gun.get_rect()
        self.rectMachine_gun.x = 1100
        self.rectMachine_gun.y = 80

        self.Shot_gun = load_image('blocks\\shot_gun_0.png')
        self.rectShot_gun = self.Shot_gun.get_rect()
        self.rectShot_gun.x = 1100
        self.rectShot_gun.y = 150

        self.flag = True
        # особое

        # кнопки
        self.text_color = '#ffffff'
        self.myfont = pygame.font.Font('media\\fonts\\quantum.otf', 20)

        self.textDef = self.myfont.render("защита", 1, self.text_color)
        self.textDefRect = self.textDef.get_rect()
        self.textDefRect.x = 250
        self.textDefRect.y = 700

        self.textAttack = self.myfont.render("оружие", 1, self.text_color)
        self.textAttackRect = self.textAttack.get_rect()
        self.textAttackRect.x = 390
        self.textAttackRect.y = 700

        self.textVip = self.myfont.render("особое", 1, self.text_color)
        self.textVipRect = self.textVip.get_rect()
        self.textVipRect.x = 530
        self.textVipRect.y = 700

        self.back = pygame.font.Font('media\\fonts\\quantum.otf', 25).render("назад", 1, '#EAFC71')
        self.backRect = self.back.get_rect()
        self.backRect.x = 25
        self.backRect.y = 845

        self.save = pygame.font.Font('media\\fonts\\quantum.otf', 20).render("сохранить", 1, '#FFB300')
        self.saveRect = self.save.get_rect()
        self.saveRect.x = 30
        self.saveRect.y = 700
        #деньги
        self.mone_icon = load_image('coin.png')
        #буфер для активного модуля
        self.aktiv_block = None
        self.sell_mode = False
        self.upgrade_mode = False
        self.duit = False
        self.buy_mode = False
            # прокачать
        self.upgrade_icon = load_image('upgrade.png')
        self.upgrade_icon_ok = load_image('upgrade_ok.png')
        self.upgrade_icon_Rect = self.upgrade_icon.get_rect()
        self.upgrade_icon_Rect.x = 745
        self.upgrade_icon_Rect.y = 240
            # продажа
        self.sell_icon = load_image('sell.png')
        self.sell_icon_ok = load_image('sell_ok.png')
        self.sell_icon_Rect = self.sell_icon.get_rect()
        self.sell_icon_Rect.x = 810
        self.sell_icon_Rect.y = 240
            # назад
        self.back_icon = load_image('back.png')
        self.back_icon_Rect = self.back_icon.get_rect()
        self.back_icon_Rect.x = 875
        self.back_icon_Rect.y = 240
        # перeтаскивание модулей
        self.update = False # обновить доску
        self.moving_item = None
        self.before_move = None
        self.can_save = False

    def defense(self, screen): #блоки брони
        screen.blit(self.Armor, (1100, 80))

    def attack(self, screen): #блоки оружия
        screen.blit(self.Machine_gun, (1100, 80))
        screen.blit(self.Shot_gun, (1100, 150))

    def vip(self, screen): #особые блоки
        screen.blit(self.Armor, (1100, 80))

    def add_botton(self, screen, mod, cash, args):
        # защита
        if self.textDefRect.collidepoint(pygame.mouse.get_pos()):
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.textDefRect.collidepoint(args[0].pos):
                mod = 1
        # оружие
        elif self.textAttackRect.collidepoint(pygame.mouse.get_pos()):
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.textAttackRect.collidepoint(args[0].pos):
                mod = 2
        # особое
        elif self.textVipRect.collidepoint(pygame.mouse.get_pos()):
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.textVipRect.collidepoint(args[0].pos):
                mod = 3
        # назад
        elif self.backRect.collidepoint(pygame.mouse.get_pos()):
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.backRect.collidepoint(args[0].pos):
                self.flag = False
                init_ship(board)

        # сохранить
        elif self.saveRect.collidepoint(pygame.mouse.get_pos()):
            if (args and args[0].type == pygame.MOUSEBUTTONDOWN and self.saveRect.collidepoint(args[0].pos) and
                    self.can_save):
                self.save_board()
        # кнопки открытого блока
        if self.aktiv_block:
            global cache, buy
            if len(self.aktiv_block) == 2:
                    # прокачка
                if self.upgrade_icon_Rect.collidepoint(pygame.mouse.get_pos()):
                    if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.upgrade_icon_Rect.collidepoint(args[0].pos):
                        if self.upgrade_mode and self.duit and board[self.aktiv_block[1][0]][self.aktiv_block[1][1]].lvl < 6:
                            board[self.aktiv_block[1][0]][self.aktiv_block[1][1]].kill()
                            cache -= board[self.aktiv_block[1][0]][self.aktiv_block[1][1]].up
                            board[self.aktiv_block[1][0]][self.aktiv_block[1][1]] =\
                                (board[self.aktiv_block[1][0]][self.aktiv_block[1][1]].__class__.__name__ + '_' +
                                 str(board[self.aktiv_block[1][0]][self.aktiv_block[1][1]].lvl + 1))
                            self.upgrade_mode = False
                            self.duit = False
                            self.update = True
                        else:
                            self.duit = False
                            self.upgrade_mode = True
                    # продажа
                if self.sell_icon_Rect.collidepoint(pygame.mouse.get_pos()):
                    if (args and args[0].type == pygame.MOUSEBUTTONDOWN and self.sell_icon_Rect.collidepoint(args[0].pos)
                            and 'Core' not in board[self.aktiv_block[1][0]][self.aktiv_block[1][1]].__class__.__name__):
                        if self.sell_mode and self.duit:
                            cache += board[self.aktiv_block[1][0]][self.aktiv_block[1][1]].sell
                            board[self.aktiv_block[1][0]][self.aktiv_block[1][1]].kill()
                            board[self.aktiv_block[1][0]][self.aktiv_block[1][1]] = 0
                            self.save_board()
                            self.sell_mode = False
                            self.aktiv_block = None
                            self.duit = False
                        else:
                            self.duit = False
                            self.sell_mode = True
            else:
                if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.sell_icon_Rect.collidepoint(args[0].pos):
                    pygame.mouse.set_pos(350, 350)
                    self.update = True
                    self.buy_mode = True
                    buy = True

        # подстановка кнопок
        screen.blit(self.textDef, (250, 700))
        pygame.draw.rect(screen, '#ffffff', (245, 700, 118, 28), 2)
        screen.blit(self.textAttack, (390, 700))
        pygame.draw.rect(screen, '#ffffff', (385, 700, 118, 28), 2)
        screen.blit(self.textVip, (530, 700))
        pygame.draw.rect(screen, '#ffffff', (525, 700, 118, 28), 2)
        screen.blit(self.back, (25, 845))
        if self.can_save: # включение кнопки сохранить
            screen.blit(self.save, (30, 700))
            pygame.draw.rect(screen, '#FFB300', (27, 695, 170, 38), 2)

        #деньги
        pygame.draw.rect(screen, '#22b14c', (1020, 20, 170, 40), 2)
        screen.blit(self.mone_icon, (1025, 25))
        screen.blit(self.myfont.render(f"{cash}", 1, self.text_color), (1058, 27))

        # кнопки активного блока
        if self.aktiv_block:
            if len(self.aktiv_block) == 2:
                    # прокачать
                if self.upgrade_mode:
                    screen.blit(self.upgrade_icon_ok, (745, 250))
                else:
                    screen.blit(self.upgrade_icon, (745, 250))
                pygame.draw.rect(screen, '#ffff00', (740, 245, 40, 40), 2)
                    # продать
                if self.sell_mode:
                    screen.blit(self.sell_icon_ok, (810, 250))
                else:
                    screen.blit(self.sell_icon, (810, 250))
                self.sell_icon_Rect.x = 810
                self.sell_icon_Rect.y = 240
                pygame.draw.rect(screen, '#22b14c', (805, 245, 40, 40), 2)
                    # убрать подробности
                screen.blit(self.back_icon, (875, 250))
                self.back_icon_Rect.x = 875
                self.back_icon_Rect.y = 240
                pygame.draw.rect(screen, '#ffffff', (870, 245, 40, 40), 2)
            else:
                    # убрать подробности
                screen.blit(self.back_icon, (840, 250))
                self.back_icon_Rect.x = 840
                self.back_icon_Rect.y = 240
                pygame.draw.rect(screen, '#ffffff', (835, 245, 40, 40), 2)
                    # купить
                screen.blit(self.sell_icon, (790, 250))
                self.sell_icon_Rect.x = 790
                self.sell_icon_Rect.y = 240
                pygame.draw.rect(screen, '#22b14c', (785, 245, 40, 40), 2)
        return mod

    def open_info(self, screen, mod, event):  # отображение активного блоки
        global move
        if event[0].type == pygame.MOUSEBUTTONDOWN and not buy:
            pos = pygame.mouse.get_pos()
            if pos[0] in range(20, 680) and pos[1] in range(20, 680):  # нажатие в пределах доски
                for y in range(11):
                    for x in range(11):
                        global board
                        if type(board[y][x]) != int:
                            if board[y][x].rect.collidepoint(pygame.mouse.get_pos()):
                                self.aktiv_block = [pygame.transform.scale(board[y][x].image, (150, 150)), [y, x]]
                                if self.timer == 0:  # запуск таймера для передвижения блока
                                    self.timer = pygame.time.get_ticks()
                                else:
                                    self.move_moduls(screen, event)
            else:  # другие нажатия
                self.timer = 0
                if self.back_icon_Rect.collidepoint(event[0].pos):
                    self.aktiv_block = None
                    move = None
                elif mod == 1:  #защитные блоки
                    if self.rectArmor.collidepoint(event[0].pos):
                        self.aktiv_block = [[pygame.transform.scale(self.Armor, (150, 150)), 'Armor_1', 500, self.Armor]]
                elif mod == 2:  #оружие
                    if self.rectMachine_gun.collidepoint(event[0].pos):
                        self.aktiv_block = [[pygame.transform.scale(self.Machine_gun, (150, 150)), 'Machine_gun_1', 750, self.Machine_gun]]
                    if self.rectShot_gun.collidepoint(event[0].pos):
                        self.aktiv_block = [[pygame.transform.scale(self.Shot_gun, (150, 150)), 'Shot_gun_1', 750, self.Shot_gun]]
        else:
            self.timer = 0
        if self.aktiv_block:
            if len(self.aktiv_block) == 2:
                # блок
                screen.blit(self.aktiv_block[0], (750, 30))
                if not move:
                    pygame.draw.rect(screen, (255, 255, 255), (self.aktiv_block[1][1] * 60 + 20, self.aktiv_block[1][0] * 60 + 20, 60, 60), 3)
            else:
                screen.blit(self.aktiv_block[0][0], (750, 30))

    def move_moduls(self, screen, event):  # передвижение модулей
        global move, board
        if move:  # если режим перемищения блока
            if event and event[0].type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]:
                board[move[1][0]][move[1][1]] = move[0]
                self.update = True
                move = None
                return
            pos = pygame.mouse.get_pos()
            if pos[0] not in range(20, 680) or pos[1] not in range(20, 680):
                board[move[1][0]][move[1][1]] = move[0]
                self.update = True
                move = None
                return
            move[0].rect.x = pos[0] - 30
            move[0].rect.y = pos[1] - 30
            if (event and event[0].type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and self.before_move
                    != pos) and board[(pos[1] - 20) // 60][(pos[0] - 20) // 60] == 1:
                board[(pos[1] - 20) // 60][(pos[0] - 20) // 60] = move[0]
                self.update = True
                move = None
                self.can_save = True
        else:  # таймер для включения режима передвижения блоков
            pos = pygame.mouse.get_pos()
            if (pygame.time.get_ticks() - self.timer)/1000 > 0.01:
                pygame.draw.arc(screen, (255, 255, 255, 100), (pos[0] - 20, pos[1] - 20, 40, 40), 0,
                                (pygame.time.get_ticks() - self.timer)/100 - 0.1, 6)
            if (pygame.time.get_ticks() - self.timer)/100 >= 6.36:
                move = [board[(pos[1] - 20) // 60][(pos[0] - 20) // 60], [(pos[1] - 20) // 60, (pos[0] - 20) // 60]]
                self.before_move = pos
                board[(pos[1] - 20) // 60][(pos[0] - 20) // 60] = 0
                self.update = True

    def save_board(self):
        global board
        cnt = [[0 for _ in range(11)] for _ in range(11)]
        for y in range(11):
            for x in range(11):
                if type(board[y][x]) != int:
                    cnt[y][x] = board[y][x].__class__.__name__ + '_' + str(board[y][x].lvl)
        cnt = ', '.join(list(map(lambda x: ', '.join(list(map(str, x))), cnt)))
        self.can_save = False
        with open('saves.txt', 'r') as f:
            data = f.readlines()
        data[0] = cnt + ' Board'
        with open('saves.txt', 'w') as f:
            f.write('\n'.join(data))

    def sell_block(self, screen, event): # отображение цены продажи
        if event and event[0].type == pygame.MOUSEBUTTONDOWN and not self.sell_icon_Rect.collidepoint(event[0].pos):
            self.sell_mode = False
        else:
            s = pygame.Surface((200, 35), pygame.SRCALPHA)
            s.fill((34, 177, 76, 50))
            pygame.draw.rect(s, (34, 177, 76), (0, 0, 200, 35), 3)
            s.blit(pygame.font.Font('media\\fonts\\quantum.otf', 12).render(f"продать за {board[self.aktiv_block[1][0]][self.aktiv_block[1][1]].sell}", 1, '#FFB300'), (10, 10))
            screen.blit(s, (725, 195))

    def upgrade(self, screen, event):
        if event and event[0].type == pygame.MOUSEBUTTONDOWN and not self.upgrade_icon_Rect.collidepoint(event[0].pos):
            self.upgrade_mode = False
        else:
            s = pygame.Surface((200, 35), pygame.SRCALPHA)
            s.fill((34, 177, 76, 50))
            pygame.draw.rect(s, (34, 177, 76), (0, 0, 200, 35), 3)
            if board[self.aktiv_block[1][0]][self.aktiv_block[1][1]].up == 0:
                s.blit(pygame.font.Font('media\\fonts\\quantum.otf', 12).render(
                    f"Максимальный ур", 1, '#FFB300'), (10, 10))
            else:
                s.blit(pygame.font.Font('media\\fonts\\quantum.otf', 12).render(f"улучшить за {board[self.aktiv_block[1][0]][self.aktiv_block[1][1]].up}", 1, '#FFB300'), (10, 10))
            screen.blit(s, (725, 195))

    def buy(self, screen, event):
        global buy, cache
        if event and event[0].type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]:
            self.buy_mode = False
            pygame.mouse.set_pos(800, 260)
            return
        pos = pygame.mouse.get_pos()
        if pos[0] not in range(20, 680) or pos[1] not in range(20, 680):
            self.buy_mode = False
            pygame.mouse.set_pos(800, 260)
            return
        screen.blit(self.aktiv_block[0][3], (pos[0] - 15, pos[1] - 15))
        if event and event[0].type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and board[(pos[1] - 20) // 60][(pos[0] - 20) // 60] == 1:
            board[(pos[1] - 20) // 60][(pos[0] - 20) // 60] = self.aktiv_block[0][1]
            self.update = True
            self.can_save = True
            self.buy_mode = False
            cache -= self.aktiv_block[0][2]
            buy = False




class Editor(pygame.sprite.Sprite):  # класс ответственный за работу редактора
    def __init__(self, *group):
        super().__init__(*group)
        self.board = Board()  # в матрицу загрузка классов блоков
        self.shop = Shop()

    def update(self, screen, *args):  # обновление скрина
        self.board.render(screen)  # рендер сетки
        self.board.test.moduls.draw(screen)  # отрисовка блоков
        self.shop.update(screen, args)  # остальная часть магазина
        if self.shop.shop_item.update:  # обновление доски перед перетаскиванием блока для появления точек
            self.board.load_bord()
            self.shop.shop_item.open_info(screen, self.shop.mod, args)
            self.shop.shop_item.update = False
            try:
                self.shop.shop_item.aktiv_block[0] = pygame.transform.scale(board[self.shop.shop_item.aktiv_block[1][0]][self.shop.shop_item.aktiv_block[1][1]].image, (150, 150))
            except Exception:
                pass
        return screen

    def restart(self):
        global board
        board = None
        self.board.load_bord()


