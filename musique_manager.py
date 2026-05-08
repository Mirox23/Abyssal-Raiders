"""
Qu'est-ce que le fichier gère : Ce fichier gère la partie musique manager du projet.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Résultat : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import pygame


class MusiqueManager:
    def __init__(self, volume=0.5):
        """
        Explication de ce que fais la fonction : Cette fonction exécute init.
        Les entrées : volume.
        Le résultat : Initialise correctement les attributs de l'objet.
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
        Explication de ce que fais la fonction : Cette fonction exécute jouer.
        Les entrées : chemin_fichier.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
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
        Explication de ce que fais la fonction : Cette fonction exécute regler volume.
        Les entrées : volume.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        self.volume = max(0.0, min(1.0, volume))
        try:
            pygame.mixer.music.set_volume(self.volume)
        except Exception:
            pass
