import os
import sys
import pygame
import random
import editor
import my_ship
from editor import Editor, save_info
from play import *
from enemy import Enemy, T_0, T_1, T_2, T_3, boss
from my_ship import *
from settings import SettingsButtons  # Импортируем настройки
pygame.init()


mode = 'menu'


def load_image(name, colorkey=None):
    fullname = os.path.join('media\\sprite', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class BeckGround(pygame.sprite.Sprite):
    bg = load_image("background.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = BeckGround.bg
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = -720

    def update(self, *args):
        if self.rect.y == 0:
            self.rect.y = -718
        else:
            self.rect.y += 1


class Main_bottons(pygame.sprite.Sprite): #класс для работы кнопок в главном меню
    def __init__(self, *group):
        self.text_color = '#EAFC71'
        self.activ_txt = '#fff200'
        super().__init__(*group)
        self.myfont = pygame.font.Font('media\\fonts\\quantum.otf', 30)
        self.myfont2 = pygame.font.Font('media\\fonts\\quantum.otf', 30)
        self.start = self.myfont.render("играть", 1, self.text_color)
        self.startRect = self.start.get_rect()
        self.startRect.x = 40
        self.startRect.y = 250
        self.edit = self.myfont.render("редактор коробля", 1, self.text_color)
        self.editRect = self.edit.get_rect()
        self.editRect.x = 40
        self.editRect.y = 310
        self.setings = self.myfont.render("настройки", 1, self.text_color)
        self.setingsRect = self.setings.get_rect()
        self.setingsRect.x = 40
        self.setingsRect.y = 370
        self.statistics = self.myfont.render("статистика", 1, self.text_color)
        self.statisticsRect = self.statistics.get_rect()
        self.statisticsRect.x = 40
        self.statisticsRect.y = 430
        self.exit = self.myfont.render("выход", 1, self.text_color)
        self.exitRect = self.exit.get_rect()
        self.exitRect.x = 40
        self.exitRect.y = 490

    def update(self, *args):
        global mode
        # кнопка начала игры
        if self.startRect.collidepoint(pygame.mouse.get_pos()):
            self.start = self.myfont2.render("играть", 1, self.activ_txt)
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.startRect.collidepoint(args[0].pos):
                mode = 'play'
        else:
            self.start = self.myfont.render("играть", 1, self.text_color)

        # кнопка редактора корабля
        if self.editRect.collidepoint(pygame.mouse.get_pos()):
            self.edit = self.myfont2.render("редактор коробля", 1, self.activ_txt)
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.editRect.collidepoint(args[0].pos):
                mode = 'edit'
                init_ship(editor.board)
                ship_editor.board.load_bord()
                ship_editor.shop.shop_item.flag = True  # флаг для выхода
                ship_editor.shop.shop_item.aktiv_block = None  # флаг для сброса активного блока
        else:
            self.edit = self.myfont.render("редактор коробля", 1, self.text_color)

        # кнопка настроек
        if self.setingsRect.collidepoint(pygame.mouse.get_pos()):
            self.setings = self.myfont2.render("настройки", 1, self.activ_txt)
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.setingsRect.collidepoint(args[0].pos):
                mode = 'settings'
        else:
            self.setings = self.myfont.render("настройки", 1, self.text_color)

        # кнопка статистики
        if self.statisticsRect.collidepoint(pygame.mouse.get_pos()):
            self.statistics = self.myfont2.render("статистика", 1, self.activ_txt)
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.statisticsRect.collidepoint(args[0].pos):
                pass
        else:
            self.statistics = self.myfont.render("статистика", 1, self.text_color)

        # кнопка выхода
        if self.exitRect.collidepoint(pygame.mouse.get_pos()):
            self.exit = self.myfont2.render("выход", 1, self.activ_txt)
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.exitRect.collidepoint(args[0].pos):
                global running
                running = False

        else:
            self.exit = self.myfont.render("выход", 1, self.text_color)

        screen.blit(self.start, (40, 250))
        screen.blit(self.edit, (40, 310))
        screen.blit(self.setings, (40, 370))
        screen.blit(self.statistics, (40, 430))
        screen.blit(self.exit, (40, 490))


if __name__ == '__main__':
    kk = 0
    pygame.display.set_caption("CoreCraft")
    screen = pygame.display.set_mode((1200, 900))
    clock = pygame.time.Clock()
    running = True
    BG = pygame.sprite.Group()
    main_bottons = pygame.sprite.Group()
    ship_editor = Editor()
    BeckGround(BG)
    Main_bottons(main_bottons)
    fps = 60
    init_ship(editor.board)
    # Добавляем группу для врагов
    enemies = pygame.sprite.Group()
    waave = 0
    type_ship = 0
    settings_buttons = SettingsButtons()
    difficulty = "normal"  # По умолчанию сложность "Нормально"
    while running:
        screen.fill((20, 20, 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_info()
                ship_editor.shop.shop_item.save_board()
                running = False
        events = pygame.event.get()
        BG.update(screen)
        BG.draw(screen)
        #проверка на рабочее окно
        if mode == 'menu':
            main_bottons.update(event)
        elif mode == 'edit':
            screen.blit(ship_editor.update(screen, event), (0, 0))
            if not ship_editor.shop.shop_item.flag:
                mode = 'menu'
        elif mode == 'play':
            waave = 0
            level, player_rect = play_mode(screen, events), play_mode(screen, events)  # Переход в режим игры
            if level:
                mode = level.lower()
                print(mode)
        elif mode == 'settings':
            result = settings_buttons.update(screen, event)
            if result in ["easy", "normal", "hard"]:
                difficulty = result
                if difficulty == "easy":
                    kk = 0.75
                if difficulty == "normal":
                    kk = 1
                if difficulty == "hard":
                    kk = 2
                print(f"Выбрана сложность: {difficulty}")
                mode = 'menu'

        # Логика для уровней
        elif mode.startswith('lvl'):
            current_level = int(mode.split(' ')[1])  # Получаем номер текущего уровня

            #столкновения
            for el in enemies:
                atk = pygame.sprite.groupcollide(el.bullets, ship_editor.board.test.moduls, True, False)
                for i in atk:
                    my_ship.xp -= 1
            for i in my_ship.canon:
                atk = pygame.sprite.groupcollide(enemies, i.bullets, False, True)
                if atk:
                    for j in atk:
                        for b in atk[j]:
                            j.take_damage(b.dmg)

            #отрисовка
            ship_editor.board.test.moduls.update()
            ship_editor.board.test.moduls.draw(screen)
            print_hp(screen)

            #проверка на колво хп
            if my_ship.xp <= 0:
                mode = 'play'

            if kk == 0:
                kk = 1
            # Переход на следующий уровень, если все враги уничтожены
            if len(enemies) == 0:
                if waave < 3:
                    waave += 1
                    mode = f'lvl {current_level}'
                else:
                    mode = 'play'  # Возвращаемся в меню после завершения всех уровней

            if len(enemies) == 0:  # Если врагов нет, создаем врагов для текущего уровня
                if current_level == 1:
                    if waave == 1:
                        enemy1 = T_0(enemies, index=0, total_enemies=1, level=1, max_health=50 * kk)
                    if waave == 2:
                        enemy1 = T_0(enemies, index=0, total_enemies=2, level=1, max_health=50 * kk)
                        enemy2 = T_0(enemies, index=1, total_enemies=2, level=1, max_health=50 * kk)
                    if waave == 3:
                        enemy1 = T_0(enemies, index=0, total_enemies=3, level=1, max_health=50 * kk)
                        enemy2 = T_1(enemies, index=1, total_enemies=3, level=1, max_health=200 * kk)
                        enemy3 = T_0(enemies, index=2, total_enemies=3, level=1, max_health=50 * kk)
                if current_level == 2:
                    if waave == 1:
                        enemy1 = T_1(enemies, index=0, total_enemies=2, level=2, max_health=500 * kk)
                        enemy2 = T_1(enemies, index=1, total_enemies=2, level=2, max_health=500 * kk)
                    if waave == 2:
                        enemy1 = T_0(enemies, index=0, total_enemies=5, level=2, max_health=300 * kk)
                        enemy2 = T_1(enemies, index=1, total_enemies=5, level=2, max_health=500 * kk)
                        enemy3 = T_1(enemies, index=2, total_enemies=5, level=2, max_health=500 * kk)
                        enemy4 = T_1(enemies, index=3, total_enemies=5, level=2, max_health=500 * kk)
                        enemy5 = T_0(enemies, index=4, total_enemies=5, level=2, max_health=300 * kk)
                    if waave == 3:
                        enemy1 = T_0(enemies, index=0, total_enemies=5, level=2, max_health=300 * kk)
                        enemy2 = T_0(enemies, index=1, total_enemies=5, level=2, max_health=300 * kk)
                        enemy3 = T_2(enemies, index=2, total_enemies=5, level=2, max_health=1000 * kk)
                        enemy4 = T_0(enemies, index=3, total_enemies=5, level=2, max_health=300 * kk)
                        enemy5 = T_0(enemies, index=4, total_enemies=5, level=2, max_health=300 * kk)

                if current_level == 3:
                    if waave == 1:
                        enemy1 = T_0(enemies, index=0, total_enemies=8, level=3, max_health=300 * kk)
                        enemy2 = T_0(enemies, index=1, total_enemies=8, level=3, max_health=300 * kk)
                        enemy3 = T_0(enemies, index=2, total_enemies=8, level=3, max_health=300 * kk)
                        enemy4 = T_0(enemies, index=3, total_enemies=8, level=3, max_health=300 * kk)
                        enemy5 = T_0(enemies, index=4, total_enemies=8, level=3, max_health=300 * kk)
                        enemy6 = T_0(enemies, index=5, total_enemies=8, level=3, max_health=300 * kk)
                        enemy7 = T_0(enemies, index=6, total_enemies=8, level=3, max_health=300 * kk)
                        enemy8 = T_0(enemies, index=7, total_enemies=8, level=3, max_health=300 * kk)
                    if waave == 2:
                        enemy1 = T_2(enemies, index=0, total_enemies=5, level=3, max_health=1000 * kk)
                        enemy2 = T_2(enemies, index=1, total_enemies=5, level=3, max_health=1000 * kk)
                        enemy3 = T_3(enemies, index=2, total_enemies=5, level=3, max_health=2000 * kk)
                        enemy4 = T_2(enemies, index=3, total_enemies=5, level=3, max_health=1000 * kk)
                        enemy5 = T_2(enemies, index=4, total_enemies=5, level=3, max_health=1000 * kk)
                if current_level == 4:
                    if waave == 1:
                        enemy1 = T_0(enemies, index=0, total_enemies=7, level=4, max_health=300 * kk)
                        enemy2 = T_1(enemies, index=1, total_enemies=7, level=4, max_health=500 * kk)
                        enemy3 = T_2(enemies, index=2, total_enemies=7, level=4, max_health=1000 * kk)
                        enemy4 = T_3(enemies, index=3, total_enemies=7, level=4, max_health=2000 * kk)
                        enemy5 = T_2(enemies, index=4, total_enemies=7, level=4, max_health=1000 * kk)
                        enemy6 = T_1(enemies, index=5, total_enemies=7, level=4, max_health=500 * kk)
                        enemy7 = T_0(enemies, index=6, total_enemies=7, level=4, max_health=300 * kk)
                    if waave == 2:
                        enemy1 = boss(enemies, index=0, total_enemies=1, level=4, max_health=5000 * kk)
            enemies.update(player_rect)
            enemies.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
    save_info()
    ship_editor.shop.shop_item.save_board()
    pygame.quit()