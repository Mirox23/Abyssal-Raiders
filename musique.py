import pygame


class MusiqueManager:
    def __init__(self, volume=0.5):
        self.volume = volume
        self.volume_effets = 0.6
        self.piste_active = None
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
        except Exception:
            pass

    def jouer(self, chemin_fichier):
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
        self.volume = max(0.0, min(1.0, volume))
        try:
            pygame.mixer.music.set_volume(self.volume)
        except Exception:
            pass

    def regler_volume_effets(self, volume):
        self.volume_effets = max(0.0, min(1.0, volume))

    def jouer_effet(self, chemin_fichier):
        """
        Joue un effet sonore court sans interrompre la musique.
        """
        try:
            son = pygame.mixer.Sound(chemin_fichier)
            son.set_volume(self.volume_effets)
            son.play()
        except Exception:
            pass

