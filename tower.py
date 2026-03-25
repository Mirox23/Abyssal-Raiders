import pygame
from setting import *
from projectile import Projectile


class Tour:
    def __init__(self, position):
        self.x, self.y = position
        self.taille = 15
        self.portee = portee_tour
        self.cadence = cadence_tour
        self.temps_depuis_tir = 0
        self.projectiles = []
        self.couleur = couleur_tour
        self.type_tour = "Base"
        self.niveau = 1

    def mettre_a_jour(self, dt, ennemis):
        self.temps_depuis_tir += dt

        if self.temps_depuis_tir >= self.cadence:
            for ennemi in ennemis:
                dx = ennemi.x - self.x
                dy = ennemi.y - self.y
                distance = (dx**2 + dy**2) ** 0.5
                if distance <= self.portee:
                    self.projectiles.append(Projectile(self.x, self.y, ennemi))
                    self.temps_depuis_tir = 0
                    break

        nouveaux = []
        for p in self.projectiles:
            p.mettre_a_jour(dt)
            if p.actif:
                nouveaux.append(p)
        self.projectiles = nouveaux

    def dessiner(self, fenetre):
        pygame.draw.circle(fenetre, self.couleur, (int(self.x), int(self.y)), self.taille)
        pygame.draw.circle(fenetre, (100, 100, 255), (int(self.x), int(self.y)), self.portee, 1)
        for p in self.projectiles:
            p.dessiner(fenetre)


class TourSniper(Tour):
    def __init__(self, position):
        super().__init__(position)
        self.couleur = (0, 0, 0)
        self.cadence = 1.5
        self.portee = 180
        self.type_tour = "Sniper"


class TourCanonnier(Tour):
    def __init__(self, position):
        super().__init__(position)
        self.couleur = (139, 69, 19)
        self.cadence = 0.5
        self.portee = 100
        self.type_tour = "Canonnier"