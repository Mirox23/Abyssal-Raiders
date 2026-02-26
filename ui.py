import pygame
from setting import *

class Button:
    def __init__(self, x, y,width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont("consolas", 20)

    def draw(self, screen, pygame):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            color = couleur_button_active
        else:
            color = couleur_button
            
        pygame.draw.rect(screen, color, self.rect)

        text_surface = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 8))