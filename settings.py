import pygame

class SettingsButtons:
    def __init__(self):
        self.text_color = '#EAFC71'  # Цвет текста по умолчанию
        self.selected_color = '#FF0000'  # Цвет выделения выбранной сложности
        self.myfont = pygame.font.Font('media\\fonts\\quantum.otf', 30)
        self.myfont2 = pygame.font.Font('media\\fonts\\quantum.otf', 30)

        # Кнопки сложности (расположены по горизонтали)
        self.easy = self.myfont.render("Легко", 1, self.text_color)
        self.easy_rect = self.easy.get_rect()
        self.easy_rect.x = 250
        self.easy_rect.y = 400

        self.normal = self.myfont.render("Нормально", 1, self.text_color)
        self.normal_rect = self.normal.get_rect()
        self.normal_rect.x = 450
        self.normal_rect.y = 400

        self.hard = self.myfont.render("Сложно", 1, self.text_color)
        self.hard_rect = self.hard.get_rect()
        self.hard_rect.x = 750
        self.hard_rect.y = 400


        # Текущая выбранная сложность
        self.selected_difficulty = "normal"  # По умолчанию "Нормально"

    def update(self, screen, event):
        # Отрисовка кнопок сложности с учетом выбранной сложности
        easy_color = self.selected_color if self.selected_difficulty == "easy" else self.text_color
        normal_color = self.selected_color if self.selected_difficulty == "normal" else self.text_color
        hard_color = self.selected_color if self.selected_difficulty == "hard" else self.text_color

        self.easy = self.myfont.render("Легко", 1, easy_color)
        self.normal = self.myfont.render("Нормально", 1, normal_color)
        self.hard = self.myfont.render("Сложно", 1, hard_color)

        screen.blit(self.easy, (250, 400))
        screen.blit(self.normal, (450, 400))
        screen.blit(self.hard, (750, 400))

        # Обработка кликов
        if event and event.type == pygame.MOUSEBUTTONDOWN:
            if self.easy_rect.collidepoint(event.pos):
                self.selected_difficulty = "easy"
                return "easy"
            elif self.normal_rect.collidepoint(event.pos):
                self.selected_difficulty = "normal"
                return "normal"
            elif self.hard_rect.collidepoint(event.pos):
                self.selected_difficulty = "hard"
                return "hard"
        return None