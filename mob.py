import pygame
import math
import random
import os

CONTINENT_MOB_ACTIF = "pirate"


def definir_continent_mob(continent):
    CONTINENT = continent or "pirate"
    globals()["CONTINENT_MOB_ACTIF"] = CONTINENT
    Mob.image_base = None
    MobRapide.image_rapide = None
    MobTank.image_tank = None
    MobKamikaze.image_kamikaze = None
    MobSoigneur.image_soigneur = None


def _charger_image_continent(nom_fichier, taille):
    essais = [
        f"image/{CONTINENT_MOB_ACTIF}/{nom_fichier}",
        f"image/{CONTINENT_MOB_ACTIF}s/{nom_fichier}",
        f"image/pirate/{nom_fichier}",
        f"image/pirates/{nom_fichier}",
    ]
    for chemin in essais:
        if os.path.exists(chemin):
            image = pygame.image.load(chemin).convert_alpha()
            return pygame.transform.scale(image, taille)
    image = pygame.Surface(taille, pygame.SRCALPHA)
    pygame.draw.circle(image, (170, 170, 190), (taille[0] // 2, taille[1] // 2), min(taille) // 2)
    return image


class Mob:
    """Mob de base : Zombie vert, vitesse normale."""
    image_base = None
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

        # flash blanc quand touché + shake 
        self.flash_timer = 0.0      # durée restante du flash blanc (en secondes)
        self.shake_timer = 0.0      # durée restante du shake (en secondes)
        self.shake_offset = (0, 0)  # décalage visuel aléatoire du shake
        self._vie_precedente = self.vie  # pour détecter les dégâts reçus
        
        # image spécifique pour le mob de base seulement
        if Mob.image_base is None:
            Mob.image_base = _charger_image_continent("Roi_des_pirates.png", (32, 32))

        self.image = Mob.image_base

    def appliquer_ralentissement(self, facteur, duree):
        """Réduit temporairement la vitesse du mob."""
        if facteur < self.facteur_ralentissement:
            self.facteur_ralentissement = facteur
            self.minuterie_ralentissement = duree

    def recevoir_degats(self, quantite):
        """Applique des dégâts et déclenche flash + shake."""
        self.vie -= quantite
        self.flash_timer = 0.08   # 80ms de flash blanc
        self.shake_timer = 0.12   # 120ms de shake
        self.shake_offset = (random.randint(-3, 3), random.randint(-3, 3))

    def avancer(self, delta_temps, chemin):
        if self.etape >= len(chemin):
            return True

        # détecter si la vie a baissé depuis la frame précédente pour déclencher le flash et le shake
        if self.vie < self._vie_precedente:
            self.flash_timer = 0.08
            self.shake_timer = 0.12
            self.shake_offset = (random.randint(-3, 3), random.randint(-3, 3))
        self._vie_precedente = self.vie

        # Mise à jour flash et shake
        if self.flash_timer > 0:
            self.flash_timer = max(0.0, self.flash_timer - delta_temps)
        if self.shake_timer > 0:
            self.shake_timer = max(0.0, self.shake_timer - delta_temps)
            if self.shake_timer > 0:
                self.shake_offset = (random.randint(-3, 3), random.randint(-3, 3))
            else:
                self.shake_offset = (0, 0)

        # Mise à jour du ralentissement
        if self.minuterie_ralentissement > 0:
            self.minuterie_ralentissement -= delta_temps
            if self.minuterie_ralentissement <= 0:
                self.facteur_ralentissement = 1.0

        # Vitesse appliquée après ralentissement éventuel.
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
        if not hasattr(self, "image") or self.image is None:
            self.image = Mob.image_base

        largeur = self.image.get_width()
        hauteur = self.image.get_height()

        image_affichee = self.image.copy()

        # Effet ralenti (teinte bleue)
        if self.facteur_ralentissement < 1.0:
            image_affichee.fill((100, 100, 255, 80), special_flags=pygame.BLEND_RGBA_ADD)

        # flash blanc quand touché
        if self.flash_timer > 0:
            image_affichee.fill((255, 255, 255, 180), special_flags=pygame.BLEND_RGBA_ADD)

        # Petite animation de flottement pour donner de la vie aux mobs
        temps_animation = pygame.time.get_ticks() * 0.01
        oscillation = math.sin(temps_animation + self.x * 0.04) * 2.2

        # shake offset sur les dégâts
        sx, sy = self.shake_offset if self.shake_timer > 0 else (0, 0)

        position_x = int(self.x - largeur // 2) + sx
        position_y = int(self.y - hauteur // 2 + oscillation) + sy
        fenetre.blit(image_affichee, (position_x, position_y))

        # Barre de vie
        largeur_barre = 30
        hauteur_barre = 4

        ratio_vie = self.vie / self.vie_max
        vie_actuelle_largeur = int(largeur_barre * ratio_vie)

        x_barre = int(self.x - largeur_barre // 2)
        y_barre = int(self.y - hauteur // 2 - 8 + oscillation)

        pygame.draw.rect(fenetre, (120, 0, 0), (x_barre, y_barre, largeur_barre, hauteur_barre))
        pygame.draw.rect(fenetre, (0, 200, 0), (x_barre, y_barre, vie_actuelle_largeur, hauteur_barre))

class MobRapide(Mob):
    """Mob rapide : bleu, peu de vie mais très véloce."""

    nom = "Rapide"
    couleur_mob = (60, 140, 230)
    vie_de_base = 2
    vitesse_de_base = 210.0
    taille_mob = 9
    recompense_mort = 3
    xp_mort = 1

    image_rapide = None

    def __init__(self, position_depart, vitesse=None, couleur=None):
        super().__init__(position_depart, vitesse, couleur)
        self.vitesse = vitesse if vitesse is not None else self.vitesse_de_base
        self.couleur = couleur if couleur is not None else self.couleur_mob
        self.taille = self.taille_mob
        self.vie_max = self.vie_de_base
        self.vie = self.vie_max
        self.recompense = self.recompense_mort
        self.xp = self.xp_mort
        
        if MobRapide.image_rapide is None:
            MobRapide.image_rapide = _charger_image_continent("Fantome_pirate.png", (28, 28))

        self.image = MobRapide.image_rapide


class MobTank(Mob):
    """Mob tank : violet foncé, beaucoup de vie, très lent."""

    nom = "Tank"
    couleur_mob = (120, 40, 160)
    vie_de_base = 20
    vitesse_de_base = 50.0
    taille_mob = 18
    recompense_mort = 6
    xp_mort = 3

    image_tank = None

    def __init__(self, position_depart, vitesse=None, couleur=None):
        super().__init__(position_depart, vitesse, couleur)
        self.vitesse = vitesse if vitesse is not None else self.vitesse_de_base
        self.couleur = couleur if couleur is not None else self.couleur_mob
        self.taille = self.taille_mob
        self.vie_max = self.vie_de_base
        self.vie = self.vie_max
        self.recompense = self.recompense_mort
        self.xp = self.xp_mort
        
        if MobTank.image_tank is None:
            MobTank.image_tank = _charger_image_continent("Triton.png", (36, 36))

        self.image = MobTank.image_tank

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

    image_kamikaze = None

    def __init__(self, position_depart, vitesse=None, couleur=None):
        super().__init__(position_depart, vitesse, couleur)
        self.vitesse = vitesse if vitesse is not None else self.vitesse_de_base
        self.couleur = couleur if couleur is not None else self.couleur_mob
        self.taille = self.taille_mob
        self.vie_max = self.vie_de_base
        self.vie = self.vie_max
        self.recompense = self.recompense_mort
        self.xp = self.xp_mort
        
        if MobKamikaze.image_kamikaze is None:
            MobKamikaze.image_kamikaze = _charger_image_continent("squelette_pirate.png", (28, 28))

        self.image = MobKamikaze.image_kamikaze

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

    image_soigneur = None

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
        
        if MobSoigneur.image_soigneur is None:
            MobSoigneur.image_soigneur = _charger_image_continent("requin.png", (28, 28))

        self.image = MobSoigneur.image_soigneur

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


class MobBoss(Mob):
    """
    Boss : apparaît à la fin du niveau (vague 4).
    Enorme PV, vitesse moyenne, récompense élevée.
    À sa mort il spawne 3 mobs normaux.
    Un halo doré l'identifie visuellement.
    """

    nom = "BOSS"
    couleur_mob = (200, 30, 200)
    vie_de_base = 70
    vitesse_de_base = 55.0
    taille_mob = 22
    recompense_mort = 20
    xp_mort = 15
    degats_mur = 5

    def __init__(self, position_depart, vitesse=None, couleur=None):
        super().__init__(position_depart, vitesse, couleur)
        self.vitesse = vitesse if vitesse is not None else self.vitesse_de_base
        self.couleur = couleur if couleur is not None else self.couleur_mob
        self.taille = self.taille_mob
        self.vie_max = self.vie_de_base
        self.vie = self.vie_max
        self.recompense = self.recompense_mort
        self.xp = self.xp_mort
        self._pulse = 0.0  # animation halo

    def avancer(self, delta_temps, chemin):
        self._pulse += delta_temps * 3.0
        return super().avancer(delta_temps, chemin)

    def dessiner(self, fenetre):
        # Halo doré autour du boss
        rayon_halo = int(self.taille + 10 + math.sin(self._pulse) * 5)
        alpha = int(120 + math.sin(self._pulse) * 60)
        surf_halo = pygame.Surface((rayon_halo * 2 + 4, rayon_halo * 2 + 4), pygame.SRCALPHA)
        pygame.draw.circle(surf_halo, (255, 200, 0, alpha), (rayon_halo + 2, rayon_halo + 2), rayon_halo, 3)
        fenetre.blit(surf_halo, (int(self.x) - rayon_halo - 2, int(self.y) - rayon_halo - 2))

        # Sprite du boss (cercle violet foncé avec taille imposante)
        super().dessiner(fenetre)

        # Label BOSS au-dessus
        police = pygame.font.SysFont("consolas", 11, bold=True)
        surf_label = police.render("⚔ BOSS ⚔", True, (255, 220, 50))
        fenetre.blit(surf_label, (int(self.x) - surf_label.get_width() // 2, int(self.y) - self.taille - 28))