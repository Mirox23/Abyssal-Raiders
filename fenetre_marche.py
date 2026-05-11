"""
A quoi sert le fichier : Ce fichier gère la fenêtre de marché qui apparaît entre les vagues pour permettre au joueur d'acheter des bonus. Il contient la classe FenetreMarcheVague qui affiche 3 cartes aléatoires avec des récompenses comme de l'or bonus, des tours gratuites, des améliorations de compétences, etc. Le joueur peut choisir une seule carte avant de continuer la partie.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu.
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
    # Classe qui gère le marché entre les vagues avec 3 cartes aléatoires
    
    """
    A quoi sert la fonction : Crée la fenêtre du marché qui propose 3 cartes aléatoires avec des bonus.
    Entrée : Cette fonction ne demande pas de paramètre direct.
    Sortie : Initialise une fenêtre de marché prête à être affichée.
    """

    def __init__(self):
        """
        A quoi sert la fonction : Initialise la fenêtre du marché avec les cartes proposées, les polices et le bouton continuer.
        Entrée : Cette fonction ne demande pas de paramètre direct.
        Sortie : Crée un objet fenêtre de marché prêt à être affiché.
        """
        self.visible = False  # État de visibilité de la fenêtre
        self.cartes_proposees = []  # Liste des cartes proposées au joueur
        self.carte_choisie = None  # Carte choisie par le joueur
        # Rectangle de positionnement de la fenêtre (centré)
        self.rect = pygame.Rect(largeur_ecran // 2 - 360, hauteur_ecran // 2 - 200, 720, 400)
        # Polices pour les différents textes
        self.police_titre = pygame.font.SysFont("consolas", 22, bold=True)  # Police pour le titre
        self.police_nom = pygame.font.SysFont("consolas", 16, bold=True)  # Police pour les noms
        self.police_desc = pygame.font.SysFont("consolas", 13)  # Police pour les descriptions
        # Bouton pour continuer après avoir choisi une carte
        self.bouton_continuer = Bouton(self.rect.centerx - 110, self.rect.bottom - 52, 220, 40, "Continuer", 17)
        self._rects_cartes = []  # Rectangles pour les cartes (calculés dynamiquement)
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
        A quoi sert la fonction : Ouvre la fenêtre du marché en générant 3 cartes aléatoires et en la rendant visible.
        Entrée : Cette fonction ne demande pas de paramètre direct.
        Sortie : Affiche la fenêtre du marché avec les cartes proposées.
        """
        self.visible = True  # Rend la fenêtre visible
        self.carte_choisie = None  # Réinitialise la carte choisie
        # Génère 3 cartes aléatoires depuis le catalogue
        self.cartes_proposees = random.sample(CATALOGUE_CARTES, min(3, len(CATALOGUE_CARTES)))
        largeur_carte = 190  # Largeur de chaque carte
        espacement = 30  # Espacement entre les cartes
        total = largeur_carte * 3 + espacement * 2  # Largeur totale occupée
        depart_x = self.rect.centerx - total // 2  # Position de départ pour centrer
        # Crée les rectangles pour les 3 cartes
        self._rects_cartes = [
            pygame.Rect(depart_x + i * (largeur_carte + espacement), self.rect.y + 65, largeur_carte, 240)
            for i in range(3)
        ]
        self.visible = True
        self.carte_choisie = None
        self.cartes_proposees = random.sample(CATALOGUE_CARTES, min(3, len(CATALOGUE_CARTES)))  # Sélectionne 3 cartes aléatoires
        largeur_carte = 190  # Largeur de chaque carte
        espacement = 30  # Espacement entre les cartes
        total = largeur_carte * 3 + espacement * 2  # Largeur totale occupée
        depart_x = self.rect.centerx - total // 2  # Position de départ pour centrer
        self._rects_cartes = [
            pygame.Rect(depart_x + i * (largeur_carte + espacement), self.rect.y + 65, largeur_carte, 240)
            for i in range(3)
        ]

    def fermer(self):
        """
        A quoi sert la fonction : Ferme la fenêtre du marché et cache la carte choisie par le joueur.
        Entrée : Cette fonction ne demande pas de paramètre direct.
        Sortie : Cache la fenêtre et efface la sélection de carte.
        """
        self.visible = False

    def gerer_clic(self, pos):
        """
        A quoi sert la fonction : Gère les clics sur les cartes du marché pour sélectionner une carte ou continuer.
        Entrée : pos (la position du clic de souris).
        Sortie : Retourne la carte choisie ou l'action 'continuer' si le bouton est cliqué.
        """
        if not self.visible:
            return None
        # Sélection d'une carte
        for i, rect in enumerate(self._rects_cartes):
            if rect.collidepoint(pos):
                self.carte_choisie = i
                return None
        # Bouton continuer : Attention ! ne fonctionne que si une carte est choisie
        if self.bouton_continuer.rect.collidepoint(pos) and self.carte_choisie is not None:  # Vérifie si le bouton continuer est cliqué et une carte est choisie
            carte = self.cartes_proposees[self.carte_choisie]
            self.fermer()
            return carte["id"]
        return None

    def dessiner(self, fenetre):
        """
        A quoi sert la fonction : Dessine la fenêtre du marché avec les 3 cartes, leurs descriptions et le bouton continuer.
        Entrée : fenetre (la surface où dessiner la fenêtre).
        Sortie : Affiche le marché avec les cartes proposées et les éléments interactifs.
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

