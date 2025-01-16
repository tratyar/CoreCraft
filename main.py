import os
import sys
import pygame
import random
from editor import Editor, save_info
pygame.init()



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
        # кнопка начала игры
        if self.startRect.collidepoint(pygame.mouse.get_pos()):
            self.start = self.myfont2.render("играть", 1, self.text_color)
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.startRect.collidepoint(args[0].pos):
                pass
        else:
            self.start = self.myfont.render("играть", 1, self.text_color)

        # кнопка редактора корабля
        if self.editRect.collidepoint(pygame.mouse.get_pos()):
            self.edit = self.myfont2.render("редактор коробля", 1, self.text_color)
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.editRect.collidepoint(args[0].pos):
                global mode
                mode = 'edit'
                ship_editor.shop.shop_item.flag = True  # флаг для выхода
                ship_editor.shop.shop_item.aktiv_block = None  # флаг для сброса активного блока
        else:
            self.edit = self.myfont.render("редактор коробля", 1, self.text_color)

        # кнопка настроек
        if self.setingsRect.collidepoint(pygame.mouse.get_pos()):
            self.setings = self.myfont2.render("настройки", 1, self.text_color)
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.setingsRect.collidepoint(args[0].pos):
                pass
        else:
            self.setings = self.myfont.render("настройки", 1, self.text_color)

        # кнопка статистики
        if self.statisticsRect.collidepoint(pygame.mouse.get_pos()):
            self.statistics = self.myfont2.render("статистика", 1, self.text_color)
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.statisticsRect.collidepoint(args[0].pos):
                pass
        else:
            self.statistics = self.myfont.render("статистика", 1, self.text_color)

        # кнопка выхода
        if self.exitRect.collidepoint(pygame.mouse.get_pos()):
            self.exit = self.myfont2.render("выход", 1, self.text_color)
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
    pygame.display.set_caption("CoreCraft")
    screen = pygame.display.set_mode((1200, 900))
    clock = pygame.time.Clock()
    running = True
    mode = 'menu'
    BG = pygame.sprite.Group()
    main_bottons = pygame.sprite.Group()
    ship_editor = Editor()
    BeckGround(BG)
    Main_bottons(main_bottons)
    fps = 60
    while running:
        screen.fill((20, 20, 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_info()
                ship_editor.shop.shop_item.save_board()
                running = False
        BG.update(screen)
        BG.draw(screen)
        #проверка на рабочее окно
        if mode == 'menu':
            main_bottons.update(event)
        if mode == 'edit':
            screen.blit(ship_editor.update(screen, event), (0, 0))
            if not ship_editor.shop.shop_item.flag:
                mode = 'menu'
        clock.tick(fps)
        pygame.display.flip()
    save_info()
    ship_editor.shop.shop_item.save_board()
    pygame.quit()