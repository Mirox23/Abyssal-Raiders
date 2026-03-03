import pygame
from setting import *


class Button:
    def __init__(self, x, y, width, height, text):

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.text = text
        self.font = pygame.font.SysFont("consolas", 20)

    def draw(self, screen):
        mouse_position = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_position):
            color = couleur_button_active
        else:
            color = couleur_button

        pygame.draw.rect(screen, color, self.rect)

        text_surface = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surface, (self.x + 10, self.y + 8))


class PhonePanel:
    def __init__(self):

        self.width = 170
        self.height_closed = 45
        self.height_open = 300

        self.x = screen_width - 190
        self.y = screen_height - 60

        self.is_open = False

        self.main_button = Button(self.x, self.y, self.width, self.height_closed, "Phone")

        # Boutons internes
        self.buttons = [
            Button(self.x, self.y - 60, self.width, 40, "Competence"),
            Button(self.x, self.y - 110, self.width, 40, "Objets"),
            Button(self.x, self.y - 160, self.width, 40, "New Manche"),
            Button(self.x, self.y - 210, self.width, 40, "Amelioration"),
            Button(self.x, self.y - 260, self.width, 40, "Parametre"),
        ]

    def handle_click(self, mouse_pos):

        # Clique sur bouton principal
        if self.main_button.rect.collidepoint(mouse_pos):
            self.is_open = not self.is_open
            return None

        # Si ouvert → vérifier boutons internes
        if self.is_open:
            for button in self.buttons:
                if button.rect.collidepoint(mouse_pos):
                    return button.text

        return None

    def draw(self, screen):

        if self.is_open:
            panel_rect = pygame.Rect(
                self.x,
                self.y - self.height_open + 45,
                self.width,
                self.height_open
            )
            pygame.draw.rect(screen, (40, 40, 50), panel_rect)

            for button in self.buttons:
                button.draw(screen)

        self.main_button.draw(screen)
