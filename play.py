import pygame


def play_mode(screen, events, unlocked_levels):
    global g
    g = ''
    button_pressed = False
    show_popup = None  # Изначально нет всплывающего окна

    # Определяем текст и прямоугольники для кнопок
    buttons = [
        {"text": "lvl 1", "pos": (300, 300), "popup": "Это уровень 1", "locked": False},
        {"text": "lvl 2", "pos": (500, 600), "popup": "Это уровень 2", "locked": not unlocked_levels["lvl 2"]},
        {"text": "lvl 3", "pos": (700, 300), "popup": "Это уровень 3", "locked": not unlocked_levels["lvl 3"]},
        {"text": "lvl 4", "pos": (900, 600), "popup": "Это уровень 4", "locked": not unlocked_levels["lvl 4"]},
        {"text": "назад", "pos": (100, 850), "popup": "Вернуться в меню", "locked": False},
    ]

    custom_font = pygame.font.Font('media/fonts/quantum.otf', 30)

    while True:
        for button in buttons:
            if button["text"] == "назад":
                button_text = custom_font.render(button["text"], True, (255, 255, 255))
            else:
                if button["locked"]:
                    button_text = pygame.font.Font(None, 120).render(button["text"], True,
                                                                     (128, 128, 128))  # Серый цвет для заблокированных
                else:
                    button_text = pygame.font.Font(None, 120).render(button["text"], True,
                                                                     (255, 255, 255))  # Обычный цвет

            button_rect = button_text.get_rect(center=button["pos"])
            mouse_pos = pygame.mouse.get_pos()

            if button_rect.collidepoint(mouse_pos) and not button["locked"]:
                if button["text"] == "назад":
                    button_text = custom_font.render(button["text"], True, (255, 255, 0))  # Цвет при наведении
                else:
                    button_text = pygame.font.Font(None, 120).render(button["text"], True,
                                                                     (255, 255, 0))  # Цвет при наведении
                show_popup = button["popup"]  # Показываем всплывающее окно
                g = button['text']
            else:
                if button["text"] == "назад":
                    button_text = custom_font.render(button["text"], True, (255, 215, 0))
                else:
                    if button["locked"]:
                        button_text = pygame.font.Font(None, 117).render(button["text"], True, (
                        128, 128, 128))  # Серый цвет для заблокированных
                    else:
                        button_text = pygame.font.Font(None, 117).render(button["text"], True, (255, 255, 255))

            screen.blit(button_text, button_rect)

            if show_popup:
                s = pygame.Surface((600, 200), pygame.SRCALPHA)  # Прозрачная поверхность
                s.fill((34, 177, 76, 20))  # Цвет фона с прозрачностью
                pygame.draw.rect(s, (34, 177, 76), (0, 0, 600, 200), 5)  # Рамка

                # Создаем текст всплывающего окна
                popup_text = pygame.font.Font('media/fonts/quantum.otf', 20).render(show_popup, True, (255, 255, 255))
                popup_rect = popup_text.get_rect(center=(300, 100))  # Центрируем текст

                # Заполняем поверхность и отображаем текст
                s.blit(popup_text, popup_rect)
                screen.blit(s, (300, 700))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if g == "назад":
                    mode = 'menu'
                    return mode  # Возвращаемся в меню
                if 'lvl' in g and not button["locked"]:  # Проверяем, не заблокирован ли уровень
                    mode = str(g)
                    return mode
                else:
                    pass
        return None  # Если нет перехода