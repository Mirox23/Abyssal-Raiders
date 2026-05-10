"""
Qu'est-ce que le fichier gère : Ce fichier gère l'initialisation de la classe Jeu.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Résultat : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import os
import pygame
from setting import largeur_ecran, hauteur_ecran
from musique import MusiqueManager


class JeuInitialisation:
    """
    Classe qui gère l'initialisation du jeu.
    Séparée de la classe principale Jeu pour respecter la limite de 300 lignes.
    """
    
    def __init__(self, continent="pirate", volume_musique=0.5, niveau=1, progression_monde=None):
        """
        Explication de ce que fais la fonction : Cette fonction exécute l'initialisation du jeu.
        Les entrées : continent, volume_musique, niveau, progression_monde.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        pygame.init()
        # Fenêtre classique (avec les boutons système Windows).
        self.fenetre = pygame.display.set_mode((largeur_ecran, hauteur_ecran), pygame.RESIZABLE)
        self.surface_logique = pygame.Surface((largeur_ecran, hauteur_ecran))
        pygame.display.set_caption("Abyssal Raiders")
        self.horloge = pygame.time.Clock()
        self.police_hud = pygame.font.SysFont("consolas", 22)
        self.police_vague = pygame.font.SysFont("consolas", 24, bold=True)
        self.continent = continent
        self.volume_musique = volume_musique
        self.niveau = niveau
        self.progression_monde = progression_monde
        self.repertoire_jeu = os.path.dirname(os.path.abspath(__file__))
        self.musique = MusiqueManager(self.volume_musique)
        self._lancer_musique_continent()
        self.image_fond = self._charger_image_fond()  # fond spécifique au continent
        
    def _charger_image_fond(self):
        """
        Explication de ce que fais la fonction : Cette fonction charge l'image de fond du continent.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Retourne l'image de fond ou None.
        """
        noms_fonds = {
            "pirate": "image/fond_pirate.png",
            "medieval": "image/fond_medieval.png", 
            "samourai": "image/fond_samourai.png",
            "demoniaque": "image/fond_demoniaque.png"
        }
        chemin_fond = noms_fonds.get(self.continent)
        if chemin_fond and os.path.exists(chemin_fond):
            try:
                img = pygame.image.load(chemin_fond).convert()
                return pygame.transform.scale(img, (largeur_ecran, hauteur_ecran))
            except Exception:
                return None
        return None
    
    def _lancer_musique_continent(self):
        """
        Explication de ce que fais la fonction : Cette fonction lance la musique du continent.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Lance la musique appropriée.
        """
        musiques_continent = {
            "pirate": "musique/pirate.mp3",
            "medieval": "musique/medieval.mp3",
            "samourai": "musique/samourai.mp3", 
            "demoniaque": "musique/demoniaque.mp3"
        }
        fichier_musique = musiques_continent.get(self.continent, "musique/pirate.mp3")
        self.musique.jouer(fichier_musique)
