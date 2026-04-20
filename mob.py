import pygame


class Mob:
    """Mob de base : Zombie vert, vitesse normale."""

    nom = "Zombie"
    couleur_mob = (60, 180, 60)
    vie_de_base = 4
    vitesse_de_base = 110.0
    taille_mob = 12
    recompense_mort = 2
    xp_mort = 1

    def __init__(self, position_depart, vitesse=None, couleur=None):
        self.x = float(position_depart[0])
        self.y = float(position_depart[1])

        self.vitesse = vitesse if vitesse is not None else self.vitesse_de_base
        self.couleur = couleur if couleur is not None else self.couleur_mob
        self.taille = self.taille_mob
        self.etape = 1
        self.vie_max = self.vie_de_base
        self.vie = self.vie_max
        self.recompense = self.recompense_mort
        self.xp = self.xp_mort

        # Ralentissement appliqué par une tour de ralentissement
        self.facteur_ralentissement = 1.0
        self.minuterie_ralentissement = 0.0

    def appliquer_ralentissement(self, facteur, duree):
        """Réduit temporairement la vitesse du mob."""
        if facteur < self.facteur_ralentissement:
            self.facteur_ralentissement = facteur
            self.minuterie_ralentissement = duree

    def avancer(self, delta_temps, chemin):
        if self.etape >= len(chemin):
            return True

        # Mise à jour du ralentissement
        if self.minuterie_ralentissement > 0:
            self.minuterie_ralentissement -= delta_temps
            if self.minuterie_ralentissement <= 0:
                self.facteur_ralentissement = 1.0

        vitesse_effective = self.vitesse * self.facteur_ralentissement

        cible_x, cible_y = chemin[self.etape]
        delta_x = cible_x - self.x
        delta_y = cible_y - self.y
        distance = (delta_x**2 + delta_y**2) ** 0.5
        deplacement = vitesse_effective * delta_temps

        if distance <= deplacement:
            self.x, self.y = cible_x, cible_y
            self.etape += 1
            return self.etape >= len(chemin)

        if distance > 0:
            self.x += (delta_x / distance) * deplacement
            self.y += (delta_y / distance) * deplacement

        return False

    def dessiner(self, fenetre):
        couleur_affichage = self.couleur
        # Teinte bleue si ralenti
        if self.facteur_ralentissement < 1.0:
            couleur_affichage = (
                max(0, self.couleur[0] - 40),
                max(0, self.couleur[1] - 20),
                min(255, self.couleur[2] + 80),
            )

        pygame.draw.circle(fenetre, couleur_affichage, (int(self.x), int(self.y)), self.taille)

        largeur_barre = 20
        hauteur_barre = 4
        ratio_vie = max(0, self.vie / self.vie_max)
        rouge = int(255 * (1 - ratio_vie))
        vert = int(255 * ratio_vie)

        barre_x = self.x - largeur_barre // 2
        barre_y = self.y - self.taille - 10
        pygame.draw.rect(fenetre, (50, 50, 50), (barre_x, barre_y, largeur_barre, hauteur_barre))
        pygame.draw.rect(fenetre, (rouge, vert, 0), (barre_x, barre_y, largeur_barre * ratio_vie, hauteur_barre))

        police_nom = pygame.font.SysFont("consolas", 9)
        surface_nom = police_nom.render(self.nom, True, (200, 200, 200))
        fenetre.blit(surface_nom, (int(self.x) - surface_nom.get_width() // 2, int(barre_y) - 10))


class MobRapide(Mob):
    """Mob rapide : bleu, peu de vie mais très véloce."""

    nom = "Rapide"
    couleur_mob = (60, 140, 230)
    vie_de_base = 2
    vitesse_de_base = 210.0
    taille_mob = 9
    recompense_mort = 3
    xp_mort = 1

    def __init__(self, position_depart, vitesse=None, couleur=None):
        super().__init__(position_depart, vitesse, couleur)
        self.vitesse = vitesse if vitesse is not None else self.vitesse_de_base
        self.couleur = couleur if couleur is not None else self.couleur_mob
        self.taille = self.taille_mob
        self.vie_max = self.vie_de_base
        self.vie = self.vie_max
        self.recompense = self.recompense_mort
        self.xp = self.xp_mort


class MobTank(Mob):
    """Mob tank : violet foncé, beaucoup de vie, très lent."""

    nom = "Tank"
    couleur_mob = (120, 40, 160)
    vie_de_base = 20
    vitesse_de_base = 50.0
    taille_mob = 18
    recompense_mort = 6
    xp_mort = 3

    def __init__(self, position_depart, vitesse=None, couleur=None):
        super().__init__(position_depart, vitesse, couleur)
        self.vitesse = vitesse if vitesse is not None else self.vitesse_de_base
        self.couleur = couleur if couleur is not None else self.couleur_mob
        self.taille = self.taille_mob
        self.vie_max = self.vie_de_base
        self.vie = self.vie_max
        self.recompense = self.recompense_mort
        self.xp = self.xp_mort


class MobKamikaze(Mob):
    """
    Mob kamikaze : orange vif, vitesse moyenne.
    Quand il atteint le mur, il explose et inflige 3 dégâts au lieu d'1.
    """

    nom = "Kamikaze"
    couleur_mob = (255, 110, 20)
    vie_de_base = 3
    vitesse_de_base = 130.0
    taille_mob = 11
    recompense_mort = 4
    xp_mort = 2
    degats_explosion = 3

    def __init__(self, position_depart, vitesse=None, couleur=None):
        super().__init__(position_depart, vitesse, couleur)
        self.vitesse = vitesse if vitesse is not None else self.vitesse_de_base
        self.couleur = couleur if couleur is not None else self.couleur_mob
        self.taille = self.taille_mob
        self.vie_max = self.vie_de_base
        self.vie = self.vie_max
        self.recompense = self.recompense_mort
        self.xp = self.xp_mort


class MobSoigneur(Mob):
    """
    Mob soigneur : croix blanche sur fond rose, vitesse lente.
    Soigne les mobs proches régulièrement.
    """

    nom = "Soigneur"
    couleur_mob = (220, 100, 160)
    vie_de_base = 6
    vitesse_de_base = 75.0
    taille_mob = 13
    recompense_mort = 5
    xp_mort = 2
    portee_soin = 80
    soin_par_tick = 1
    cadence_soin = 2.0

    def __init__(self, position_depart, vitesse=None, couleur=None):
        super().__init__(position_depart, vitesse, couleur)
        self.vitesse = vitesse if vitesse is not None else self.vitesse_de_base
        self.couleur = couleur if couleur is not None else self.couleur_mob
        self.taille = self.taille_mob
        self.vie_max = self.vie_de_base
        self.vie = self.vie_max
        self.recompense = self.recompense_mort
        self.xp = self.xp_mort
        self.minuterie_soin = 0.0

    def soigner_alentours(self, delta_temps, liste_ennemis):
        """Soigne les mobs proches toutes les cadence_soin secondes."""
        self.minuterie_soin += delta_temps
        if self.minuterie_soin >= self.cadence_soin:
            self.minuterie_soin = 0.0
            for autre_mob in liste_ennemis:
                if autre_mob is self:
                    continue
                distance = ((autre_mob.x - self.x)**2 + (autre_mob.y - self.y)**2) ** 0.5
                if distance <= self.portee_soin:
                    autre_mob.vie = min(autre_mob.vie_max, autre_mob.vie + self.soin_par_tick)

    def dessiner(self, fenetre):
        super().dessiner(fenetre)
        # Croix blanche pour identifier le soigneur
        centre_x = int(self.x)
        centre_y = int(self.y)
        pygame.draw.line(fenetre, (255, 255, 255), (centre_x - 5, centre_y), (centre_x + 5, centre_y), 2)
        pygame.draw.line(fenetre, (255, 255, 255), (centre_x, centre_y - 5), (centre_x, centre_y + 5), 2)