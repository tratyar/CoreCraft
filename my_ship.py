import pygame.mouse
xp = 0

xp_icon = pygame.image.load('media/sprite/xp.png')


waypoint = ['Shot_gun', 'Machine_gun']
canon = []


def init_ship(data):
    global xp
    canon.clear()
    xp = 0
    for el in data:
        for i in el:
            if type(i) != int:
                i.revers_mod()
                if i.__class__.__name__ in waypoint:
                    canon.append(i)
                try:
                    xp += i.xp
                except Exception:
                    pass


def print_hp(screen):
    for i in range(xp):
        screen.blit(xp_icon, (10 + (3 + 22) * i, 10))