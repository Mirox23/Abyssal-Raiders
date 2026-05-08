"""
Qu'est-ce que le fichier gère : Ce fichier gère la partie musique du projet.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Résultat : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import os
import pygame


MUSIQUES = {
    "menu": "menu.mp3",
    "jeu": "jeu.mp3",
    "boss": "boss.mp3",
}


class MusiqueManager:
    """Gestion simple de la musique et des effets sonores."""

    def __init__(self, volume=0.5):
        """
        Explication de ce que fais la fonction : Cette fonction exécute init.
        Les entrées : volume.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        self.volume = max(0.0, min(1.0, volume))
        self.volume_effets = 0.6
        self.piste_active = None
        self.repertoire_jeu = os.path.dirname(os.path.abspath(__file__))
        self.dossier_musique = os.path.join(self.repertoire_jeu, "musique")

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
        except Exception:
            pass

    def _resolver_fichier_audio(self, fichier_audio):
        """
        Explication de ce que fais la fonction : Cette fonction exécute resolver fichier audio.
        Les entrées : fichier_audio.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        fichier_audio = MUSIQUES.get(fichier_audio, fichier_audio)

        if os.path.isabs(fichier_audio):
            return fichier_audio

        if fichier_audio.startswith("musique" + os.sep) or fichier_audio.startswith("musique/"):
            return os.path.join(self.repertoire_jeu, fichier_audio)

        return os.path.join(self.dossier_musique, fichier_audio)

    def jouer(self, fichier_audio):
        """
        Explication de ce que fais la fonction : Cette fonction exécute jouer.
        Les entrées : fichier_audio.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        fichier_audio = self._resolver_fichier_audio(fichier_audio)
        if self.piste_active == fichier_audio:
            return
        if not os.path.exists(fichier_audio):
            self.piste_active = None
            return
        try:
            pygame.mixer.music.load(fichier_audio)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1)
            self.piste_active = fichier_audio
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

    def regler_volume_effets(self, volume):
        """
        Explication de ce que fais la fonction : Cette fonction exécute regler volume effets.
        Les entrées : volume.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        self.volume_effets = max(0.0, min(1.0, volume))

    def jouer_effet(self, fichier_audio):
        """
        Explication de ce que fais la fonction : Cette fonction exécute jouer effet.
        Les entrées : fichier_audio.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        fichier_audio = self._resolver_fichier_audio(fichier_audio)
        if not os.path.exists(fichier_audio):
            return
        try:
            son = pygame.mixer.Sound(fichier_audio)
            son.set_volume(self.volume_effets)
            son.play()
        except Exception:
            pass

