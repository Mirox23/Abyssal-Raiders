import pygame
from setting import couleur_button, couleur_button_active


class Button:
    def __init__(self, x, y, largeur, hauteur, texte):

        self.zone = pygame.Rect(x, y, largeur, hauteur)
        self.texte = texte
        self.police = pygame.font.SysFont("consolas", 20)

    def draw(self, screen):

        mouse_position = pygame.mouse.get_pos()

        if self.zone.collidepoint(mouse_position):
            couleur = couleur_button_active
        else:
            couleur = couleur_button

        pygame.draw.rect(screen, couleur, self.zone)

        texte_surface = self.police.render(self.texte, True, (255, 255, 255))
        screen.blit(texte_surface, (self.zone.x + 10, self.zone.y + 8))