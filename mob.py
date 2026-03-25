import pygame


class Mob:
    """Mob de base : Zombie vert, vitesse normale"""

    nom = "Zombie"
    couleur_mob = (60, 180, 60)
    vie_de_base = 4
    vitesse_de_base = 110.0
    taille_mob = 12
    recompense_mort = 2

    def __init__(self, position_depart, vitesse=None, couleur=None):
        self.x = float(position_depart[0])
        self.y = float(position_depart[1])

        if vitesse is not None:
            self.vitesse = vitesse
        else:
            self.vitesse = self.vitesse_de_base

        if couleur is not None:
            self.couleur = couleur
        else:
            self.couleur = self.couleur_mob

        self.taille = self.taille_mob
        self.etape = 1
        self.vie_max = self.vie_de_base
        self.vie = self.vie_max
        self.recompense = self.recompense_mort

    def avancer(self, delta_temps, chemin):
        if self.etape >= len(chemin):
            return True

        cible_x, cible_y = chemin[self.etape] #point de chemin que le mob doit atteindre pour avancer à l'étape suivante
        delta_x = cible_x - self.x
        delta_y = cible_y - self.y
        distance = (delta_x**2 + delta_y**2) ** 0.5
        deplacement = self.vitesse * delta_temps

        if distance <= deplacement:
            self.x, self.y = cible_x, cible_y
            self.etape += 1
            return self.etape >= len(chemin)

        if distance > 0:
            self.x += (delta_x / distance) * deplacement
            self.y += (delta_y / distance) * deplacement

        return False

    def dessiner(self, fenetre):
        pygame.draw.circle(fenetre, self.couleur, (int(self.x), int(self.y)), self.taille)

        largeur_barre = 20
        hauteur_barre = 4
        ratio_vie = max(0, self.vie / self.vie_max)
        rouge = int(255 * (1 - ratio_vie))
        vert = int(255 * ratio_vie)

        barre_x = self.x - largeur_barre // 2
        barre_y = self.y - self.taille - 10
        pygame.draw.rect(fenetre, (50, 50, 50), (barre_x, barre_y, largeur_barre, hauteur_barre)) #fond gris de la barre de vie
        pygame.draw.rect(fenetre, (rouge, vert, 0), (barre_x, barre_y, largeur_barre * ratio_vie, hauteur_barre)) #partie colorée de la barre de vie

        police_nom = pygame.font.SysFont("consolas", 9) #consolas pour un style pixelisé
        surface_nom = police_nom.render(self.nom, True, (200, 200, 200))
        fenetre.blit(surface_nom, (int(self.x) - surface_nom.get_width() // 2, int(barre_y) - 10))


class MobRapide(Mob):
    """Mob rapide : bleu, peu de vie mais très rapide"""

    nom = "Rapide"
    couleur_mob = (60, 140, 230)
    vie_de_base = 2
    vitesse_de_base = 210.0
    taille_mob = 9
    recompense_mort = 3

    def __init__(self, position_depart, vitesse=None, couleur=None):
        super().__init__(position_depart, vitesse, couleur)
        if vitesse is None:
            self.vitesse = self.vitesse_de_base
        if couleur is None:
            self.couleur = self.couleur_mob
        self.taille = self.taille_mob
        self.vie_max = self.vie_de_base
        self.vie = self.vie_max
        self.recompense = self.recompense_mort