import pygame
from setting import portee_tour, cadence_tour, couleur_tour, cout_amelioration, bonus_portee, bonus_cadence, niveau_max
from projectile import Projectile


class Tour:
    def __init__(self, position):
        self.x, self.y = position
        self.taille = 15
        self.portee = portee_tour
        self.cadence = cadence_tour
        self.temps_depuis_dernier_tir = 0
        self.liste_projectiles = []
        self.couleur = couleur_tour
        self.type_tour = "Base"
        self.niveau = 1

    def ameliorer(self, argent_joueur):
        if self.niveau >= niveau_max:
            return -1
        if argent_joueur < cout_amelioration:
            return -1
        self.niveau += 1
        self.portee += bonus_portee
        self.cadence = max(0.15, self.cadence - bonus_cadence)
        return argent_joueur - cout_amelioration

    def mettre_a_jour(self, delta_temps, liste_ennemis):
        self.temps_depuis_dernier_tir += delta_temps

        if self.temps_depuis_dernier_tir >= self.cadence:
            for ennemi in liste_ennemis:
                delta_x = ennemi.x - self.x
                delta_y = ennemi.y - self.y
                distance = (delta_x**2 + delta_y**2) ** 0.5
                if distance <= self.portee:
                    nouveau_projectile = Projectile(self.x, self.y, ennemi)
                    self.liste_projectiles.append(nouveau_projectile)
                    self.temps_depuis_dernier_tir = 0
                    break

        projectiles_actifs = []
        for projectile in self.liste_projectiles:
            projectile.mettre_a_jour(delta_temps)
            if projectile.actif:
                projectiles_actifs.append(projectile)
        self.liste_projectiles = projectiles_actifs

    def dessiner(self, fenetre):
        pygame.draw.circle(fenetre, self.couleur, (int(self.x), int(self.y)), self.taille)
        pygame.draw.circle(fenetre, (80, 80, 160), (int(self.x), int(self.y)), self.portee, 1)

        police_niveau = pygame.font.SysFont("consolas", 10, bold=True)
        surface_niveau = police_niveau.render(str(self.niveau), True, (0, 0, 0))
        fenetre.blit(surface_niveau, (
            int(self.x) - surface_niveau.get_width() // 2,
            int(self.y) - surface_niveau.get_height() // 2
        ))

        for projectile in self.liste_projectiles:
            projectile.dessiner(fenetre)


class TourSniper(Tour):
    def __init__(self, position):
        super().__init__(position)
        self.couleur = (20, 20, 20)
        self.cadence = 1.5
        self.portee = 250
        self.type_tour = "Sniper"


class TourCanonnier(Tour):
    def __init__(self, position):
        super().__init__(position)
        self.couleur = (139, 69, 19)
        self.cadence = 0.5
        self.portee = 100
        self.type_tour = "Canonnier"