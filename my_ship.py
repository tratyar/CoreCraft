import pygame.mouse

xp = 0
max_xp = 0

xp_icon = pygame.image.load('media/sprite/xp.png')

waypoint = ['Shot_gun', 'Machine_gun', 'Laser']
canon = []


def init_ship(data):
    global xp, max_xp
    canon.clear()
    xp = 0
    for el in data:
        for i in el:
            if type(i) != int:
                i.revers_mod()
                if i.__class__.__name__ in waypoint:
                    canon.append(i)
                else:
                    xp += i.xp
    max_xp = xp


def print_hp(screen):
    for i in range(xp):
        screen.blit(xp_icon, (10 + (3 + 22) * i, 10))
