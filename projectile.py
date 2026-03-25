import pygame
from setting import vitesse_projectile, taille_projectile


class Projectile:
    def __init__(self, depart_x, depart_y, cible): #le projectile part de la position de la tour et se dirige vers un ennemi spécifique : la "cibe"
        self.x = depart_x
        self.y = depart_y
        self.cible = cible
        self.vitesse = vitesse_projectile
        self.taille = taille_projectile
        self.actif = True

    def mettre_a_jour(self, delta_temps):
        if not self.cible or self.cible.vie <= 0:
            self.actif = False
            return

        delta_x = self.cible.x - self.x
        delta_y = self.cible.y - self.y
        distance = (delta_x**2 + delta_y**2) ** 0.5

        if distance < 5:
            self.cible.vie -= 1
            self.actif = False
            return

        if distance > 0:
            self.x += (delta_x / distance) * self.vitesse * delta_temps #delta_x / distance est la direction du projectile, multipliée par la vitesse et le temps écoulé pour que le mouvement soit fluide et indépendant du nombre de frames par seconde
            self.y += (delta_y / distance) * self.vitesse * delta_temps

    def dessiner(self, fenetre):
        pygame.draw.circle(fenetre, (255, 220, 50), (int(self.x), int(self.y)), self.taille)