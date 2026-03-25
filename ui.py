import pygame
from setting import *


class Bouton:
    def __init__(self, x, y, largeur, hauteur, texte):
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.texte = texte
        self.police = pygame.font.SysFont("consolas", 20)

    def dessiner(self, fenetre):
        pos_souris = pygame.mouse.get_pos()
        couleur = couleur_bouton_survol if self.rect.collidepoint(pos_souris) else couleur_bouton
        pygame.draw.rect(fenetre, couleur, self.rect)
        surface_texte = self.police.render(self.texte, True, (255, 255, 255))
        fenetre.blit(surface_texte, (self.x + 10, self.y + 8))


class PanneauTelephone:
    def __init__(self):
        self.largeur = 170
        self.hauteur_ferme = 45
        self.hauteur_ouvert = 300

        self.x = largeur_ecran - 190
        self.y = hauteur_ecran - 60

        self.ouvert = False

        self.bouton_principal = Bouton(self.x, self.y, self.largeur, self.hauteur_ferme, "Phone")

        self.liste_boutons = [
            Bouton(self.x, self.y - 60,  self.largeur, 40, "Competence"),
            Bouton(self.x, self.y - 110, self.largeur, 40, "Objets"),
            Bouton(self.x, self.y - 160, self.largeur, 40, "New Manche"),
            Bouton(self.x, self.y - 210, self.largeur, 40, "Amelioration"),
            Bouton(self.x, self.y - 260, self.largeur, 40, "Parametre"),
        ]

    def gerer_clic(self, pos_clic):
        if self.bouton_principal.rect.collidepoint(pos_clic):
            self.ouvert = not self.ouvert
            return None

        if self.ouvert:
            for btn in self.liste_boutons:
                if btn.rect.collidepoint(pos_clic):
                    return btn.texte

        return None

    def dessiner(self, fenetre):
        if self.ouvert:
            fond = pygame.Rect(self.x, self.y - self.hauteur_ouvert + 45, self.largeur, self.hauteur_ouvert)
            pygame.draw.rect(fenetre, (40, 40, 50), fond)
            for btn in self.liste_boutons:
                btn.dessiner(fenetre)

        self.bouton_principal.dessiner(fenetre)