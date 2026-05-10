"""
A quoi sert le fichier : Ce fichier gère le système de musique et d'effets sonores du jeu. Il contient la classe MusiqueManager qui permet de jouer les musiques de fond selon le contexte (menu, jeu, boss), de régler le volume, de jouer des effets sonores, et de gérer les chemins des fichiers audio. Il assure aussi l'initialisation correcte du système audio de Pygame.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu.
"""

# Importe les bibliothèques nécessaires pour la gestion audio
import os
import pygame


# Dictionnaire des musiques disponibles avec leurs noms de fichiers
MUSIQUES = {
    "menu": "menu.mp3",      # Musique du menu principal
    "jeu": "jeu.mp3",        # Musique pendant les vagues normales
    "boss": "boss.mp3",       # Musique pendant les vagues de boss
}


class MusiqueManager:
    # Classe qui gère la musique et les effets sonores du jeu
    """Gestion simple de la musique et des effets sonores."""

    def __init__(self, volume=0.5):
        """
        A quoi sert la fonction : Initialise le gestionnaire de musique avec le volume donné.
        Entrée : volume.
        Sortie : Initialise correctement les attributs de l'objet.
        """
        self.volume = max(0.0, min(1.0, volume))  # Limite le volume entre 0 et 1
        self.volume_effets = 0.6  # Volume des effets sonores (fixe)
        self.piste_active = None  # Piste de musique actuellement jouée
        self.repertoire_jeu = os.path.dirname(os.path.abspath(__file__))  # Chemin du dossier du jeu
        self.dossier_musique = os.path.join(self.repertoire_jeu, "musique")  # Dossier des musiques
        
        # Initialise le système audio de Pygame si nécessaire
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
        except Exception:
            pass

    def _resolver_fichier_audio(self, fichier_audio):
        """
        A quoi sert la fonction : Résout le chemin complet d'un fichier audio.
        Entrée : fichier_audio.
        Sortie : Retourne la valeur attendue ou applique l'action prévue.
        """
        # Cherche le fichier audio dans le dictionnaire des musiques
        fichier_audio = MUSIQUES.get(fichier_audio, fichier_audio)

        # Si le chemin est déjà absolu, le retourne tel quel
        if os.path.isabs(fichier_audio):
            return fichier_audio
        
        # Si le fichier commence par "musique" ou "musique/", construit le chemin complet
        if fichier_audio.startswith("musique" + os.sep) or fichier_audio.startswith("musique/"):
            return os.path.join(self.repertoire_jeu, fichier_audio)
        
        # Sinon, cherche dans le dossier musique
        return os.path.join(self.dossier_musique, fichier_audio)

    def jouer(self, fichier_audio):
        """
        A quoi sert la fonction : Joue une musique de fond en boucle.
        Entrée : fichier_audio.
        Sortie : Retourne la valeur attendue ou applique l'action prévue.
        """
        fichier_audio = self._resolver_fichier_audio(fichier_audio)  # Résout le chemin complet
        
        # Vérifie si le fichier existe
        if not os.path.exists(fichier_audio):
            print(f"ERREUR MUSIQUE: Fichier non trouvé - {fichier_audio}")
            return
        
        try:
            # Diagnostic: vérifier l'état de pygame.mixer
            if not pygame.mixer.get_init():
                print("ERREUR MUSIQUE: pygame.mixer non initialisé, tentative d'initialisation...")
                pygame.mixer.init()
            
            print(f"DIAGNOSTIC MUSIQUE: Tentative de lecture - {fichier_audio}")
            pygame.mixer.music.load(fichier_audio)  # Charge le fichier audio
            pygame.mixer.music.set_volume(self.volume)  # Applique le volume
            pygame.mixer.music.play(-1)  # Joue en boucle infinie
            self.piste_active = fichier_audio  # Mémorise la piste active
            print(f"DIAGNOSTIC MUSIQUE: Lecture démarrée avec succès - {fichier_audio}")
        except Exception as e:
            print(f"ERREUR MUSIQUE: Impossible de jouer {fichier_audio} - {e}")
            self.piste_active = None

    def regler_volume(self, volume):
        """
        A quoi sert la fonction : Règle le volume de la musique de fond.
        Entrée : volume.
        Sortie : Retourne la valeur attendue ou applique l'action prévue.
        """
        self.volume = max(0.0, min(1.0, volume))  # Limite le volume entre 0 et 1
        try:
            pygame.mixer.music.set_volume(self.volume)  # Applique le volume à la musique
        except Exception:
            pass  # Ignore les erreurs si la musique n'est pas initialisée

    def regler_volume_effets(self, volume):
        """
        A quoi sert la fonction : Règle le volume des effets sonores.
        Entrée : volume.
        Sortie : Retourne la valeur attendue ou applique l'action prévue.
        """
        self.volume_effets = max(0.0, min(1.0, volume))  # Limite le volume entre 0 et 1

    def jouer_effet(self, fichier_audio):
        """
        A quoi sert la fonction : Joue un effet sonore unique.
        Entrée : fichier_audio.
        Sortie : Retourne la valeur attendue ou applique l'action prévue.
        """
        fichier_audio = self._resolver_fichier_audio(fichier_audio)  # Résout le chemin complet
        if not os.path.exists(fichier_audio):  # Vérifie si le fichier existe
            return  # Sort silencieusement si le fichier n'existe pas
        
        try:
            son = pygame.mixer.Sound(fichier_audio)  # Crée un objet son
            son.set_volume(self.volume_effets)  # Applique le volume des effets
            son.play()  # Joue l'effet
        except Exception:
            pass  # Ignore les erreurs de lecture audio

