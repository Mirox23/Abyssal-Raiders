import pygame
from setting import vitesse_projectile, taille_projectile


class Projectile:
    def __init__(self, dep_x, dep_y, cible):
        self.x = dep_x
        self.y = dep_y
        self.cible = cible

        self.vitesse = vitesse_projectile
        self.taille = taille_projectile

        self.actif = True

    def mettre_a_jour(self, dt):
        if not self.cible or self.cible.vie <= 0:
            self.actif = False
            return

        dx = self.cible.x - self.x
        dy = self.cible.y - self.y
        distance = (dx**2 + dy**2) ** 0.5

        if distance < 5:
            self.cible.vie -= 1
            self.actif = False
            return

        if distance > 0:
            self.x += (dx / distance) * self.vitesse * dt
            self.y += (dy / distance) * self.vitesse * dt

    def dessiner(self, fenetre):
        pygame.draw.circle(fenetre, (255, 220, 50), (int(self.x), int(self.y)), self.taille)