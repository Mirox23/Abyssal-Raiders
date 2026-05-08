"""
Qu'est-ce que le fichier gère : Ce fichier gère la partie fenetre marche du projet.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Résultat : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import pygame
import random
from interface import Bouton
from setting import largeur_ecran, hauteur_ecran

# Marché entre les vagues

CATALOGUE_CARTES = [
    {"id": "or_bonus", "nom": "+20 Or", "desc": "Coffre de butin pirate", "cout": 0,  "couleur": (200, 170, 40)},
    {"id": "soin_mur", "nom": "+3 Vie mur","desc": "Planches de renfort", "cout": 0,  "couleur": (80, 180, 100)},
    {"id": "tour_gratuite", "nom": "Tour offerte", "desc": "Pose une tour sans payer", "cout": 0, "couleur": (100, 140, 220)},
    {"id": "cadence_bonus", "nom": "Cadence +15%", "desc": "Huile de mecanique magique", "cout": 0, "couleur": (220, 120, 50)},
    {"id": "portee_bonus", "nom": "Portée +20","desc": "Longue-vue enchantée", "cout": 0, "couleur": (160, 80, 200)},
    {"id": "xp_bonus", "nom": "+25 XP", "desc": "Parchemin de sagesse", "cout": 0, "couleur": (80, 200, 210)},
    {"id": "argent_double", "nom": "Primes x2 (vague)", "desc": "Contrat de mercenaire", "cout": 0, "couleur": (255, 200, 0)},
    {"id": "gel_global", "nom": "Gel de zone", "desc": "Blizzard instantané", "cout": 0, "couleur": (150, 200, 255)},
]


class FenetreMarcheVague:
    """
    Marché entre les vagues : 3 cartes aléatoires apparaissent,
    le joueur en choisit UNE. Puis il clique 'Continuer'.
    """

    def __init__(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute init.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        self.visible = False
        self.cartes_proposees = []
        self.carte_choisie = None
        self.rect = pygame.Rect(largeur_ecran // 2 - 360, hauteur_ecran // 2 - 200, 720, 400)
        self.police_titre = pygame.font.SysFont("consolas", 22, bold=True)
        self.police_nom = pygame.font.SysFont("consolas", 16, bold=True)
        self.police_desc = pygame.font.SysFont("consolas", 13)
        self.bouton_continuer = Bouton(self.rect.centerx - 110, self.rect.bottom - 52, 220, 40, "Continuer", 17)
        self._rects_cartes = []

    def ouvrir(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute ouvrir.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        self.visible = True
        self.carte_choisie = None
        self.cartes_proposees = random.sample(CATALOGUE_CARTES, min(3, len(CATALOGUE_CARTES)))
        largeur_carte = 190
        espacement = 30
        total = largeur_carte * 3 + espacement * 2
        depart_x = self.rect.centerx - total // 2
        self._rects_cartes = [
            pygame.Rect(depart_x + i * (largeur_carte + espacement), self.rect.y + 65, largeur_carte, 240)
            for i in range(3)
        ]

    def fermer(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute fermer.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        self.visible = False

    def gerer_clic(self, pos):
        """
        Explication de ce que fais la fonction : Cette fonction gère gerer clic en fonction du contexte courant.
        Les entrées : pos.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if not self.visible:
            return None
        # Sélection d'une carte
        for i, rect in enumerate(self._rects_cartes):
            if rect.collidepoint(pos):
                self.carte_choisie = i
                return None
        # Bouton continuer : Attention ! ne fonctionne que si une carte est choisie
        if self.bouton_continuer.rect.collidepoint(pos) and self.carte_choisie is not None:
            carte = self.cartes_proposees[self.carte_choisie]
            self.fermer()
            return carte["id"]
        return None

    def dessiner(self, fenetre):
        """
        Explication de ce que fais la fonction : Cette fonction dessine dessiner à l'écran.
        Les entrées : fenetre.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if not self.visible:
            return
        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 155))
        fenetre.blit(voile, (0, 0))
        pygame.draw.rect(fenetre, (18, 22, 36), self.rect, border_radius=14)
        pygame.draw.rect(fenetre, (100, 130, 200), self.rect, width=2, border_radius=14)
        titre = self.police_titre.render("⚓ Marché du butin : choisissez une récompense", True, (220, 210, 80))
        fenetre.blit(titre, (self.rect.centerx - titre.get_width() // 2, self.rect.y + 14))

        for i, (carte, rect) in enumerate(zip(self.cartes_proposees, self._rects_cartes)):
            selectionne = i == self.carte_choisie
            couleur_fond = (35, 42, 62) if not selectionne else (50, 60, 95)
            couleur_bord = carte["couleur"] if selectionne else (70, 85, 130)
            epaisseur_bord = 3 if selectionne else 1
            pygame.draw.rect(fenetre, couleur_fond, rect, border_radius=12)
            pygame.draw.rect(fenetre, couleur_bord, rect, width=epaisseur_bord, border_radius=12)

            # Icone de couleur en haut
            pygame.draw.rect(fenetre, carte["couleur"], pygame.Rect(rect.x + 16, rect.y + 18, rect.width - 32, 50), border_radius=8)

            surf_nom = self.police_nom.render(carte["nom"], True, (255, 255, 255) if selectionne else (210, 210, 210))
            fenetre.blit(surf_nom, (rect.centerx - surf_nom.get_width() // 2, rect.y + 82))
            surf_desc = self.police_desc.render(carte["desc"], True, (170, 185, 210))
            fenetre.blit(surf_desc, (rect.centerx - surf_desc.get_width() // 2, rect.y + 108))

            if selectionne:
                surf_ok = self.police_desc.render("✓ Sélectionnée", True, (130, 230, 140))
                fenetre.blit(surf_ok, (rect.centerx - surf_ok.get_width() // 2, rect.y + 135))

        if self.carte_choisie is not None:
            self.bouton_continuer.dessiner(fenetre)
        else:
            # Bouton grisé
            pygame.draw.rect(fenetre, (50, 55, 70), self.bouton_continuer.rect, border_radius=5)
            surf = self.police_desc.render("Choisissez une carte", True, (130, 130, 150))
            fenetre.blit(surf, (self.bouton_continuer.rect.centerx - surf.get_width() // 2,
                                self.bouton_continuer.rect.centery - surf.get_height() // 2))

