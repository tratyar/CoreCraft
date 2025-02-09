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
    # В начале файла, рядом с другими глобальными переменными
    unlocked_levels = {"lvl 1": True, "lvl 2": False, "lvl 3": False,
                       "lvl 4": True}  # По умолчанию открыт только первый уровень
    wave_text_alpha = 0  # Начальная прозрачность текста
    wave_text_fade_in = True  # Флаг для появления текста
    wave_text_fade_out = False  # Флаг для исчезания текста
    wave_text_surface = None
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
    # Переменные для задержки между волнами
    wave_delay = 3000  # Задержка в миллисекундах (3 секунды)
    wave_start_time = 0
    show_wave_text = False

    # Переменные для отображения результата игры
    game_over = False
    game_result = None  # "win" или "lose"
    result_display_time = 0
    result_delay = 3000  # Задержка перед возвращением в меню (3 секунды)
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

            # Столкновения
            for el in enemies:
                # Обработка столкновений обычных снарядов врагов с модулями корабля игрока
                atk = pygame.sprite.groupcollide(el.bullets, ship_editor.board.test.moduls, True, False)
                for i in atk:
                    my_ship.xp -= 1  # Обычные снаряды наносят 1 HP урона

                # Обработка столкновений синих снарядов босса с модулями корабля игрока
                if isinstance(el, boss):  # Проверяем, что это босс
                    blue_atk = pygame.sprite.groupcollide(el.blue_bullets, ship_editor.board.test.moduls, True, False)
                    for i in blue_atk:
                        my_ship.xp -= 2  # Синие снаряды наносят 2 HP урона

                # Обработка столкновений снарядов игрока с врагами
                for i in my_ship.canon:
                    atk = pygame.sprite.groupcollide(enemies, i.bullets, False, True)
                    if atk:
                        for j in atk:
                            for b in atk[j]:
                                j.take_damage(b.dmg)  # Наносим урон врагу

            #отрисовка
            ship_editor.board.test.moduls.update()
            ship_editor.board.test.moduls.draw(screen)
            print_hp(screen)

            # Проверка на количество HP
            if my_ship.xp <= 0:
                for enemy in enemies:
                    enemy.kill()
                game_over = True
                game_result = "lose"  # Поражение
                result_display_time = pygame.time.get_ticks()

            if kk == 0:
                kk = 1

            # Переход на следующую волну, если все враги уничтожены
            if len(enemies) == 0 and not show_wave_text:
                if (waave < 3 and current_level < 3) or (waave < 2 and current_level > 2):
                    waave += 1
                    wave_start_time = pygame.time.get_ticks()  # Запоминаем время начала задержки
                    show_wave_text = True  # Показываем текст о начале волны
                else:
                    game_over = True
                    waave = 0
                    game_result = "win"  # Победа
                    result_display_time = pygame.time.get_ticks()

                    # Если идет задержка между волнами
                    if show_wave_text:
                        current_time = pygame.time.get_ticks()
                        if current_time - wave_start_time < wave_delay:
                            # Создаем поверхность для текста с прозрачностью, если она еще не создана

                            wave_font = pygame.font.Font('media\\fonts\\quantum.otf', 50)
                            wave_text = wave_font.render(f"Волна {waave}", True, (255, 255, 255))
                            wave_text_surface = pygame.Surface(wave_text.get_size(), pygame.SRCALPHA)
                            wave_text_surface.blit(wave_text, (0, 0))  # Рисуем текст на поверхности
                            wave_text_rect = wave_text_surface.get_rect(center=(600, 450))  # Центрируем текст

                            # Плавное появление текста
                            if wave_text_fade_in:
                                wave_text_alpha += 3.9  # Увеличиваем прозрачность
                                if wave_text_alpha >= 255:
                                    wave_text_alpha = 255
                                    wave_text_fade_in = False
                                    wave_text_fade_out = True  # Начинаем исчезание

                            # Плавное исчезание текста
                            if wave_text_fade_out:
                                wave_text_alpha -= 3.9  # Уменьшаем прозрачность
                                if wave_text_alpha <= 0:
                                    wave_text_alpha = 0
                                    wave_text_fade_in = False
                                    wave_text_fade_out = False

                            # Устанавливаем прозрачность текста и отображаем его
                            if wave_text_surface:  # Проверяем, что поверхность создана
                                wave_text_surface.set_alpha(wave_text_alpha)  # Применяем прозрачность
                                screen.blit(wave_text_surface, wave_text_rect)
                        else:
                            wave_text_fade_in = True
                            show_wave_text = False

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

                    # Отображение результата игры
                    if game_over:
                        current_time = pygame.time.get_ticks()
                        if current_time - result_display_time < result_delay:
                            # Отображаем текст "Победа" или "Поражение"
                            result_font = pygame.font.Font('media\\fonts\\quantum.otf', 50)
                            if game_result == "win":
                                mode = "win"
                                if current_level < 4:  # Если это не последний уровень
                                    next_level = f"lvl {current_level + 1}"  # Следующий уровень
                                    unlocked_levels[next_level] = True
                                my_ship.xp = my_ship.max_xp
                                result_text = result_font.render("Победа!", True, (0, 255, 0))
                            else:
                                my_ship.xp = my_ship.max_xp
                                mode = 'porajenie'
                                waave = 0
                                result_text = result_font.render("Поражение!", True, (255, 0, 0))
                            text_rect = result_text.get_rect(center=(600, 450))
                            screen.blit(result_text, text_rect)
                        else:
                            # Возвращаемся в меню после задержки
                            for enemy in enemies:
                                enemy.kill()
                            game_over = False
                            mode = 'menu'

            enemies.update(player_rect)
            enemies.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
    save_info()
    ship_editor.shop.shop_item.save_board()
    pygame.quit()