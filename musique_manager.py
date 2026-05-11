"""
A quoi sert le fichier : Ce fichier gère la lecture et le contrôle des fichiers musicaux du jeu. Il contient la classe MusiqueManager qui permet de jouer des musiques de fond, de contrôler le volume, de gérer les transitions entre morceaux, et d'assurer que l'audio est correctement initialisé. Il gère aussi l'arrêt et la reprise de la musique selon le contexte du jeu.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import pygame


class MusiqueManager:
    def __init__(self, volume=0.5):
        """
        A quoi sert la fonction : Initialise le gestionnaire de musique avec le volume spécifié et prépare le système audio.
        Entrée : volume (le volume audio initial entre 0.0 et 1.0, par défaut 0.5).
        Sortie : Crée un objet MusiqueManager prêt à jouer des musiques.
        """
        self.volume = volume
        self.piste_active = None
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
        except Exception:
            pass

    def jouer(self, chemin_fichier):
        """
        A quoi sert la fonction : Joue un fichier musical en boucle avec le volume actuel et gère les erreurs de chargement.
        Entrée : chemin_fichier (le chemin complet du fichier musical à jouer).
        Sortie : Charge et joue la musique en boucle, ou arrête la musique si erreur.
        """
        if self.piste_active == chemin_fichier:
            return
        try:
            pygame.mixer.music.load(chemin_fichier)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1)
            self.piste_active = chemin_fichier
        except Exception:
            self.piste_active = None

    def regler_volume(self, volume):
        """
        A quoi sert la fonction : Ajuste le volume audio entre 0.0 et 1.0 et l'applique immédiatement à la musique en cours.
        Entrée : volume (le nouveau volume audio entre 0.0 et 1.0).
        Sortie : Met à jour le volume et l'applique à la musique actuelle.
        """
        self.volume = max(0.0, min(1.0, volume))
        try:
            pygame.mixer.music.set_volume(self.volume)
        except Exception:
            pass
