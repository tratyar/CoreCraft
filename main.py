import pygame
import sys
import os
import random
import math
import editor
import my_ship
from editor import Editor, save_info
from play import *
from enemy import Enemy, T_0, T_1, T_2, T_3, boss
from my_ship import *
from settings import SettingsButtons

pygame.init()

mode = 'menu'


def project(vector, w, h, fov, distance):
    factor = math.atan(fov / 2 * math.pi / 180) / (distance + vector.z)
    x = vector.x * factor * w + w / 2
    y = -vector.y * factor * w + h / 2
    return pygame.math.Vector3(x, y, vector.z)


def rotate_vertices(vertices, angle, axis):
    return [v.rotate(angle, axis) for v in vertices]


def scale_vertices(vertices, s):
    return [pygame.math.Vector3(v[0] * s[0], v[1] * s[1], v[2] * s[2]) for v in vertices]


def translate_vertices(vertices, t):
    return [v + pygame.math.Vector3(t) for v in vertices]


def project_vertices(vertices, w, h, fov, distance):
    return [project(v, w, h, fov, distance) for v in vertices]


class Mesh():

    def __init__(self, vertices, faces):
        self.__vertices = [pygame.math.Vector3(v) for v in vertices]
        self.__faces = faces

    def rotate(self, angle, axis):
        self.__vertices = rotate_vertices(self.__vertices, angle, axis)

    def scale(self, s):
        self.__vertices = scale_vertices(self.__vertices, s)

    def translate(self, t):
        self.__vertices = translate_vertices(self.__vertices, t)

    def calculate_average_z(self, vertices):
        return [(i, sum([vertices[j].z for j in f]) / len(f)) for i, f in enumerate(self.__faces)]

    def get_face(self, index):
        return self.__faces[index]

    def get_vertices(self):
        return self.__vertices

    def create_polygon(self, face, vertices):
        return [(vertices[i].x, vertices[i].y) for i in [*face, face[0]]]


class Scene:
    def __init__(self, mehses, fov, distance):
        self.meshes = mehses
        self.fov = fov
        self.distance = distance
        self.euler_angles = [0, 0, 0]
        self.move = 1
        self.color = [255, 0, 0]

    def set_colot(self):
        if self.color[0] == 255:
            self.move = -1
        elif self.color[0] == 0:
            self.move = 1
        self.color[0] += self.move
        self.color[2] -= self.move

    def transform_vertices(self, vertices, width, height):
        transformed_vertices = vertices
        axis_list = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
        for angle, axis in reversed(list(zip(list(self.euler_angles), axis_list))):
            transformed_vertices = rotate_vertices(transformed_vertices, angle, axis)
        transformed_vertices = project_vertices(transformed_vertices, width, height, self.fov, self.distance)
        return transformed_vertices

    def draw(self, surface):

        polygons = []
        for mesh in self.meshes:
            transformed_vertices = self.transform_vertices(mesh.get_vertices(), *surface.get_size())
            avg_z = mesh.calculate_average_z(transformed_vertices)
            for z in avg_z:
                pointlist = mesh.create_polygon(mesh.get_face(z[0]), transformed_vertices)
                polygons.append((pointlist, z[1]))
        for poly in sorted(polygons, key=lambda x: x[1], reverse=True):
            pygame.draw.polygon(surface, self.color, poly[0])
            pygame.draw.polygon(surface, (0, 0, 0), poly[0], 1)
        self.set_colot()


vertices = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1), (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
            (-2, 1, -1)]
faces = [(0, 1, 2, 3), (1, 5, 6, 2), (5, 4, 7, 6), (4, 0, 3, 7), (3, 2, 6, 7), (1, 0, 4, 5)]

cube_origins = [(-3, 0, 0), (3, 0, 0), (0, 0, 4), (0, 0, -4), (-3, 1, 0), (3, 1, 0), (0, 1, 3), (0, 1, -3), (-3, -1, 0),
                (3, -1, 0), (0, -1, 3), (0, -1, -3),
                (-2, 2, 0), (-2, -2, 0), (2, 2, 0), (2, -2, 0), (0, 1, 2), (0, -1, 2), (0, 1, -2), (0, -1, -2),
                (2, 3, 0), (2, -3, 0), (-2, 3, 0), (-2, -3, 0), (1, 4, 0), (1, -4, 0), (-1, 4, 0), (-1, -4, 0),
                (0, 2, 0), (0, 2, 1), (0, 2, -1), (0, -2, 0), (0, -2, 1), (0, -2, -1), (0, 5, 0), (0, -5, 0)]
meshes = []
for origin in cube_origins:
    cube = Mesh(vertices, faces)
    cube.scale((0.35, 0.35, 0.35))
    cube.translate(origin)
    meshes.append(cube)

scene = Scene(meshes, 90, 10)


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


class Main_bottons(pygame.sprite.Sprite):
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
        if self.startRect.collidepoint(pygame.mouse.get_pos()):
            self.start = self.myfont2.render("играть", 1, self.activ_txt)
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.startRect.collidepoint(args[0].pos):
                mode = 'play'
        else:
            self.start = self.myfont.render("играть", 1, self.text_color)

        if self.editRect.collidepoint(pygame.mouse.get_pos()):
            self.edit = self.myfont2.render("редактор коробля", 1, self.activ_txt)
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.editRect.collidepoint(args[0].pos):
                mode = 'edit'
                init_ship(editor.board)
                ship_editor.shop.shop_item.flag = True
                ship_editor.shop.shop_item.aktiv_block = None
                ship_editor.board.load_bord()
        else:
            self.edit = self.myfont.render("редактор коробля", 1, self.text_color)

        if self.setingsRect.collidepoint(pygame.mouse.get_pos()):
            self.setings = self.myfont2.render("настройки", 1, self.activ_txt)
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.setingsRect.collidepoint(args[0].pos):
                mode = 'settings'
        else:
            self.setings = self.myfont.render("настройки", 1, self.text_color)

        if self.statisticsRect.collidepoint(pygame.mouse.get_pos()):
            self.statistics = self.myfont2.render("статистика", 1, self.activ_txt)
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.statisticsRect.collidepoint(args[0].pos):
                pass
        else:
            self.statistics = self.myfont.render("статистика", 1, self.text_color)

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
    xss = 0
    # В начале файла, рядом с другими глобальными переменными
    unlocked_levels = {"lvl 1": True, "lvl 2": False, "lvl 3": False,
                       "lvl 4": True}  # По умолчанию открыт только первый уровень
    wave_text_alpha = 0  # Начальная прозрачность текста
    wave_text_fade_in = True  # Флаг для появления текста
    wave_text_fade_out = False  # Флаг для исчезания текста
    wave_text_surface = None
    kk = 1
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
    enemies = pygame.sprite.Group()
    waave = 0
    settings_buttons = SettingsButtons()
    difficulty = "normal"

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

        if mode == 'menu':
            main_bottons.update(event)
            s = pygame.Surface((600, 600), pygame.SRCALPHA)
            scene.draw(s)
            scene.euler_angles[1] += 1
            screen.blit(s, (550, 150))
            screen.blit(pygame.font.Font('media\\fonts\\quantum.otf', 50).render("CoreCraft", 1, '#fff200'), (40, 180))
        elif mode == 'edit':
            screen.blit(ship_editor.update(screen, event), (0, 0))
            if not ship_editor.shop.shop_item.flag:
                mode = 'menu'
        elif mode == 'play':
            waave = 0
            level, player_rect = play_mode(screen, events, unlocked_levels, kk), play_mode(screen, events,
                                                                                           unlocked_levels, kk)
            if level:
                mode = level.lower()
                print(mode)
        elif mode == 'settings':
            result = settings_buttons.update(screen, event)
            if result in ["easy", "normal", "hard"]:
                difficulty = result
                if difficulty == "easy":
                    kk = 0.5
                if difficulty == "normal":
                    kk = 1
                if difficulty == "hard":
                    kk = 2
                print(f"Выбрана сложность: {difficulty}")
                mode = 'menu'

        # Логика для уровней
        elif mode.startswith('lvl'):
            current_level = int(mode.split(' ')[1])

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

            # Отрисовка
            ship_editor.board.test.moduls.update()
            ship_editor.board.test.moduls.draw(screen)
            print_hp(screen)

            # Проверка на количество HP
            if my_ship.xp <= 0:
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

            # Создание врагов для текущей волны
            if len(enemies) == 0 and not show_wave_text:
                if current_level == 1:
                    xss = 0
                    if waave == 1:
                        enemy1 = T_0(enemies, index=0, total_enemies=1, level=1, max_health=300 * kk)
                    if waave == 2:
                        enemy1 = T_0(enemies, index=0, total_enemies=2, level=1, max_health=300 * kk)
                        enemy2 = T_0(enemies, index=1, total_enemies=2, level=1, max_health=300 * kk)
                    if waave == 3:
                        enemy1 = T_0(enemies, index=0, total_enemies=3, level=1, max_health=300 * kk)
                        enemy2 = T_1(enemies, index=1, total_enemies=3, level=1, max_health=500 * kk)
                        enemy3 = T_0(enemies, index=2, total_enemies=3, level=1, max_health=300 * kk)

                if current_level == 2:
                    xss = 0
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
                    xss = 0
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
                    xss = 0
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

        # Отображение результата игры
        if game_over:
            if xss == 0:
                if current_level == 1:
                    editor.cache += (1000 * kk)
                if current_level == 2:
                    editor.cache += (2000 * kk)
                if current_level == 3:
                    editor.cache += (3000 * kk)
                if current_level == 4:
                    editor.cache += (4000 * kk)
                xss += 1
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
                    for enemy in enemies:
                        enemy.kill()
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

        clock.tick(fps)
        pygame.display.flip()

    save_info()
    ship_editor.shop.shop_item.save_board()
    pygame.quit()
