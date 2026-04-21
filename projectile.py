import pygame
from setting import vitesse_projectile, taille_projectile


class Projectile:
    def __init__(self, depart_x, depart_y, cible):
        self.x = depart_x
        self.y = depart_y
        self.cible = cible
        self.vitesse = vitesse_projectile
        self.taille = taille_projectile
        self.actif = True
        self.degats = 1
        self.couleur_projectile = (255, 220, 50)

    def mettre_a_jour(self, delta_temps):
        if not self.cible or self.cible.vie <= 0:
            self.actif = False
            return

        delta_x = self.cible.x - self.x
        delta_y = self.cible.y - self.y
        distance = (delta_x**2 + delta_y**2) ** 0.5

        if distance < 5:
            self.cible.vie -= self.degats
            self.actif = False
            return

        if distance > 0:
            self.x += (delta_x / distance) * self.vitesse * delta_temps
            self.y += (delta_y / distance) * self.vitesse * delta_temps

    def dessiner(self, fenetre):
        pygame.draw.circle(fenetre, (255, 255, 255), (int(self.x), int(self.y)), self.taille + 2, 1)
        pygame.draw.circle(fenetre, self.couleur_projectile, (int(self.x), int(self.y)), self.taille)


class ProjectileRalentissement(Projectile):
    """Projectile qui ralentit la cible à l'impact."""

    def __init__(self, depart_x, depart_y, cible, facteur_ralentissement, duree_ralentissement):
        super().__init__(depart_x, depart_y, cible)
        self.facteur_ralentissement = facteur_ralentissement
        self.duree_ralentissement = duree_ralentissement
        self.couleur_projectile = (100, 180, 255)
        self.degats = 1

    def mettre_a_jour(self, delta_temps):
        if not self.cible or self.cible.vie <= 0:
            self.actif = False
            return

        delta_x = self.cible.x - self.x
        delta_y = self.cible.y - self.y
        distance = (delta_x**2 + delta_y**2) ** 0.5

        if distance < 5:
            self.cible.vie -= self.degats
            self.cible.appliquer_ralentissement(self.facteur_ralentissement, self.duree_ralentissement)
            self.actif = False
            return

        if distance > 0:
            self.x += (delta_x / distance) * self.vitesse * delta_temps
            self.y += (delta_y / distance) * self.vitesse * delta_temps