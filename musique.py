import os
import pygame


MUSIQUES = {
    "menu": ("menu.wav", "menu.mp3"),
    "jeu": ("jeu.wav", "jeu.mp3"),
    "boss1": ("boss1.wav", "boss1.mp3"),
    "boss2": ("boss2.wav", "boss2.mp3"),
}


class MusiqueManager:
    """Gestion simple de la musique et des effets sonores."""

    def __init__(self, volume=0.5):
        self.volume = max(0.0, min(1.0, volume))
        self.volume_effets = 0.6
        self.piste_active = None
        self.repertoire_jeu = os.path.dirname(os.path.abspath(__file__))
        self.dossier_musique = os.path.join(self.repertoire_jeu, "musique")

        self._preparer_mixer()

    def _preparer_mixer(self):
        """Demarre le mixer de pygame si besoin."""
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.pre_init(44100, -16, 2, 512)
                pygame.mixer.init()
            return True
        except Exception as erreur:
            print("Erreur mixer :", erreur)
            return False

    def _resolver_fichier_audio(self, fichier_audio):
        """Retourne le chemin du fichier audio dans le dossier musique."""
        fichiers_possibles = MUSIQUES.get(fichier_audio, (fichier_audio,))
        if isinstance(fichiers_possibles, str):
            fichiers_possibles = (fichiers_possibles,)

        for fichier_possible in fichiers_possibles:
            if os.path.isabs(fichier_possible):
                if os.path.exists(fichier_possible):
                    return fichier_possible
                continue

            if fichier_possible.startswith("musique" + os.sep) or fichier_possible.startswith("musique/"):
                chemin = os.path.join(self.repertoire_jeu, fichier_possible)
            else:
                chemin = os.path.join(self.dossier_musique, fichier_possible)

            if os.path.exists(chemin):
                return chemin

        # Si rien n'existe, on garde le premier chemin pour aider au debug.
        premier_fichier = fichiers_possibles[0]
        if os.path.isabs(premier_fichier):
            return premier_fichier
        return os.path.join(self.dossier_musique, premier_fichier)

    def jouer(self, fichier_audio, fondu_ms=0, forcer=False):
        if not self._preparer_mixer():
            return

        fichier_audio = self._resolver_fichier_audio(fichier_audio)
        meme_piste = self.piste_active == fichier_audio
        if meme_piste and pygame.mixer.music.get_busy() and not forcer:
            return
        if not os.path.exists(fichier_audio):
            self.piste_active = None
            print("Musique introuvable :", fichier_audio)
            return
        try:
            if self.piste_active and not meme_piste and fondu_ms > 0 and pygame.mixer.music.get_busy():
                pygame.mixer.music.fadeout(fondu_ms)
                pygame.time.delay(fondu_ms)
            pygame.mixer.music.load(fichier_audio)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1, fade_ms=fondu_ms)
            self.piste_active = fichier_audio
        except Exception as erreur:
            self.piste_active = None
            print("Erreur musique :", erreur)

    def garantir(self, fichier_audio):
        """Relance la musique demandee si elle s'est arretee."""
        fichier_audio = self._resolver_fichier_audio(fichier_audio)
        if self.piste_active != fichier_audio or not pygame.mixer.music.get_busy():
            self.jouer(fichier_audio, fondu_ms=500, forcer=True)

    def regler_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
        try:
            pygame.mixer.music.set_volume(self.volume)
        except Exception:
            pass

    def regler_volume_effets(self, volume):
        self.volume_effets = max(0.0, min(1.0, volume))

    def jouer_effet(self, fichier_audio):
        """Joue un effet court sans interrompre la musique de fond."""
        fichier_audio = self._resolver_fichier_audio(fichier_audio)
        if not os.path.exists(fichier_audio):
            return
        try:
            son = pygame.mixer.Sound(fichier_audio)
            son.set_volume(self.volume_effets)
            son.play()
        except Exception:
            pass
