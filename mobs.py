"""
Qu'est-ce que le fichier gère : Ce fichier gère la partie mobs principaux du projet.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Résultat : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import pygame
import math
import random
import os
import unicodedata

CONTINENT_MOB_ACTIF = "pirate"
REPERTOIRE_JEU = os.path.dirname(os.path.abspath(__file__))
DOSSIER_IMAGE = os.path.join(REPERTOIRE_JEU, "image")

NOMS_SPRITES_PAR_CONTINENT = {
    "pirate": {
        "base": ["Roi_des_pirates.png"],
        "rapide": ["Fantome_pirate.png"],
        "tank": ["Triton.png"],
        "kamikaze": ["squelette_pirate.png"],
        "soigneur": ["Requin.png", "requin.png"],
    },
    "samourai": {
        "base": ["Oni.png"],
        "rapide": ["loup spirituel.png"],
        "tank": ["Sprite boss monde Samurai 1.png"],
        "kamikaze": ["marionette.png"],
        "soigneur": ["Serpent.png"],
    },
    "medieval": {
        "base": ["Chevalier corrompu.png"],
        "rapide": ["bandit masqué.png"],
        "tank": ["Chevalier sans tete.png"],
        "kamikaze": ["Archer maléfique.png"],
        "soigneur": ["Paysan possede.png"],
    },
    "demoniaque": {
        "base": ["Demon fantome.png"],
        "rapide": ["Demon chauve souris.png"],
        "tank": ["Demon lourd.png"],
        "kamikaze": ["Demon sorcier.png"],
        "soigneur": ["Sprite boss monde volcanique 1.png"],
    },
}


def _normaliser_texte(texte):
    """
    Explication de ce que fais la fonction : Cette fonction exécute normaliser texte.
    Les entrées : texte.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
    texte_nfd = unicodedata.normalize("NFKD", texte)
    caracteres = []
    for caractere in texte_nfd:
        if not unicodedata.combining(caractere):
            caracteres.append(caractere)
    return "".join(caracteres).lower()


def definir_continent_mob(continent):
    """
    Explication de ce que fais la fonction : Cette fonction définit definir continent mob.
    Les entrées : continent.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
    continent_brut = continent or "pirate"
    continent_normalise = _normaliser_texte(continent_brut)
    if continent_normalise not in NOMS_SPRITES_PAR_CONTINENT:
        continent_normalise = "pirate"
    CONTINENT = continent_normalise
    globals()["CONTINENT_MOB_ACTIF"] = CONTINENT
    Mob.image_base = None
    MobRapide.image_rapide = None
    MobTank.image_tank = None
    MobKamikaze.image_kamikaze = None
    MobSoigneur.image_soigneur = None


def _dossiers_possibles_continent():
    """
    Explication de ce que fais la fonction : Cette fonction exécute dossiers possibles continent.
    Les entrées : Cette fonction ne demande pas de paramètre direct.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
    dossiers = []
    dossier_principal = CONTINENT_MOB_ACTIF
    dossiers.append(os.path.join(DOSSIER_IMAGE, dossier_principal))
    dossiers.append(os.path.join(DOSSIER_IMAGE, dossier_principal + "s"))
    if CONTINENT_MOB_ACTIF == "demoniaque":
        dossiers.append(os.path.join(DOSSIER_IMAGE, "démoniaque"))
    return dossiers


def _charger_image_continent(type_sprite, taille):
    """
    Explication de ce que fais la fonction : Cette fonction exécute charger image continent.
    Les entrées : type_sprite, taille.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
    candidats = []
    noms_par_type = NOMS_SPRITES_PAR_CONTINENT.get(CONTINENT_MOB_ACTIF, {})
    if type_sprite in noms_par_type:
        for nom in noms_par_type[type_sprite]:
            candidats.append(nom)
    if CONTINENT_MOB_ACTIF != "pirate":
        for nom in NOMS_SPRITES_PAR_CONTINENT["pirate"].get(type_sprite, []):
            candidats.append(nom)

    for dossier in _dossiers_possibles_continent():
        for nom_fichier in candidats:
            chemin = os.path.join(dossier, nom_fichier)
            if os.path.exists(chemin):
                try:
                    image = pygame.image.load(chemin).convert_alpha()
                    return pygame.transform.scale(image, taille)
                except Exception:
                    continue

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
        """
        Explication de ce que fais la fonction : Cette fonction exécute init.
        Les entrées : position_depart, vitesse, couleur.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
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
            Mob.image_base = _charger_image_continent("base", (32, 32))

        self.image = Mob.image_base

    def appliquer_ralentissement(self, facteur, duree):
        """
        Explication de ce que fais la fonction : Cette fonction exécute appliquer ralentissement.
        Les entrées : facteur, duree.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if facteur < self.facteur_ralentissement:
            self.facteur_ralentissement = facteur
            self.minuterie_ralentissement = duree

    def recevoir_degats(self, quantite):
        """
        Explication de ce que fais la fonction : Cette fonction exécute recevoir degats.
        Les entrées : quantite.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        self.vie -= quantite
        self.flash_timer = 0.08   # 80ms de flash blanc
        self.shake_timer = 0.12   # 120ms de shake
        self.shake_offset = (random.randint(-3, 3), random.randint(-3, 3))

    def avancer(self, delta_temps, chemin):
        """
        Explication de ce que fais la fonction : Cette fonction exécute avancer.
        Les entrées : delta_temps, chemin.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
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
        """
        Explication de ce que fais la fonction : Cette fonction dessine dessiner à l'écran.
        Les entrées : fenetre.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
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
        """
        Explication de ce que fais la fonction : Cette fonction exécute init.
        Les entrées : position_depart, vitesse, couleur.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        super().__init__(position_depart, vitesse, couleur)
        self.vitesse = vitesse if vitesse is not None else self.vitesse_de_base
        self.couleur = couleur if couleur is not None else self.couleur_mob
        self.taille = self.taille_mob
        self.vie_max = self.vie_de_base
        self.vie = self.vie_max
        self.recompense = self.recompense_mort
        self.xp = self.xp_mort
        
        if MobRapide.image_rapide is None:
            MobRapide.image_rapide = _charger_image_continent("rapide", (28, 28))

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
        """
        Explication de ce que fais la fonction : Cette fonction exécute init.
        Les entrées : position_depart, vitesse, couleur.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        super().__init__(position_depart, vitesse, couleur)
        self.vitesse = vitesse if vitesse is not None else self.vitesse_de_base
        self.couleur = couleur if couleur is not None else self.couleur_mob
        self.taille = self.taille_mob
        self.vie_max = self.vie_de_base
        self.vie = self.vie_max
        self.recompense = self.recompense_mort
        self.xp = self.xp_mort
        
        if MobTank.image_tank is None:
            MobTank.image_tank = _charger_image_continent("tank", (36, 36))

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
        """
        Explication de ce que fais la fonction : Cette fonction exécute init.
        Les entrées : position_depart, vitesse, couleur.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        super().__init__(position_depart, vitesse, couleur)
        self.vitesse = vitesse if vitesse is not None else self.vitesse_de_base
        self.couleur = couleur if couleur is not None else self.couleur_mob
        self.taille = self.taille_mob
        self.vie_max = self.vie_de_base
        self.vie = self.vie_max
        self.recompense = self.recompense_mort
        self.xp = self.xp_mort
        
        if MobKamikaze.image_kamikaze is None:
            MobKamikaze.image_kamikaze = _charger_image_continent("kamikaze", (28, 28))

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
        """
        Explication de ce que fais la fonction : Cette fonction exécute init.
        Les entrées : position_depart, vitesse, couleur.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
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
            MobSoigneur.image_soigneur = _charger_image_continent("soigneur", (28, 28))

        self.image = MobSoigneur.image_soigneur

    def soigner_alentours(self, delta_temps, liste_ennemis):
        """
        Explication de ce que fais la fonction : Cette fonction exécute soigner alentours.
        Les entrées : delta_temps, liste_ennemis.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
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
        """
        Explication de ce que fais la fonction : Cette fonction dessine dessiner à l'écran.
        Les entrées : fenetre.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
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
    taille_mob = 34
    recompense_mort = 20
    xp_mort = 15
    degats_mur = 5

    def __init__(self, position_depart, vitesse=None, couleur=None):
        """
        Explication de ce que fais la fonction : Cette fonction exécute init.
        Les entrées : position_depart, vitesse, couleur.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        super().__init__(position_depart, vitesse, couleur)
        self.vitesse = vitesse if vitesse is not None else self.vitesse_de_base
        self.couleur = couleur if couleur is not None else self.couleur_mob
        self.taille = self.taille_mob
        self.vie_max = self.vie_de_base
        self.vie = self.vie_max
        self.recompense = self.recompense_mort
        self.xp = self.xp_mort
        self._pulse = 0.0  # animation halo

        # Boss visuellement plus grand que les autres mobs.
        if self.image is not None:
            self.image = pygame.transform.scale(self.image, (72, 72))

    def avancer(self, delta_temps, chemin):
        """
        Explication de ce que fais la fonction : Cette fonction exécute avancer.
        Les entrées : delta_temps, chemin.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        self._pulse += delta_temps * 3.0
        return super().avancer(delta_temps, chemin)

    def dessiner(self, fenetre):
        """
        Explication de ce que fais la fonction : Cette fonction dessine dessiner à l'écran.
        Les entrées : fenetre.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
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