"""
Qu'est-ce que le fichier gère : Ce fichier gère la partie fenetre fin vague du projet.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Résultat : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import pygame
from interface import Bouton
from setting import largeur_ecran, hauteur_ecran

class EcranFinVague:
    def __init__(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute init.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        self.visible = False
        self.numero_vague = 0
        self.xp_gagnee = 0
        self.score_vague = 0
        self.police_titre = pygame.font.SysFont("consolas", 30, bold=True)
        self.police_message = pygame.font.SysFont("consolas", 19)
        self.police_xp = pygame.font.SysFont("consolas", 16)
        centre_x = largeur_ecran // 2
        centre_y = hauteur_ecran // 2
        self.rect = pygame.Rect(centre_x - 250, centre_y - 115, 500, 230)
        self.bouton_nouvelle_vague = Bouton(centre_x - 230, centre_y + 60, 210, 44, "Nouvelle vague", 18)
        self.bouton_modification = Bouton(centre_x + 20, centre_y + 60, 210, 44, "Modification", 18)

    def ouvrir(self, numero, xp_gagnee, score_vague):
        """
        Explication de ce que fais la fonction : Cette fonction exécute ouvrir.
        Les entrées : numero, xp_gagnee, score_vague.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        self.numero_vague = numero
        self.xp_gagnee = xp_gagnee
        self.score_vague = score_vague
        self.visible = True

    def fermer(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute fermer.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        self.visible = False

    def gerer_clic(self, position_clic):
        """
        Explication de ce que fais la fonction : Cette fonction gère gerer clic en fonction du contexte courant.
        Les entrées : position_clic.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if not self.visible:
            return None
        if self.bouton_nouvelle_vague.rect.collidepoint(position_clic):
            return "nouvelle_vague"
        if self.bouton_modification.rect.collidepoint(position_clic):
            return "modification"
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
        voile.fill((0, 0, 0, 140))
        fenetre.blit(voile, (0, 0))
        pygame.draw.rect(fenetre, (28, 32, 46), self.rect, border_radius=12)
        pygame.draw.rect(fenetre, (100, 120, 200), self.rect, width=2, border_radius=12)
        centre_x = self.rect.centerx
        surface_titre = self.police_titre.render("Félicitations !", True, (210, 200, 80))
        fenetre.blit(surface_titre, (centre_x - surface_titre.get_width() // 2, self.rect.y + 18))
        surface_message = self.police_message.render(f"Vous avez terminé la vague {self.numero_vague} !", True, (200, 200, 200))
        fenetre.blit(surface_message, (centre_x - surface_message.get_width() // 2, self.rect.y + 62))
        surface_xp = self.police_xp.render(f"+ {self.xp_gagnee} XP gagnés pour cette vague", True, (100, 210, 255))
        fenetre.blit(surface_xp, (centre_x - surface_xp.get_width() // 2, self.rect.y + 90))
        surface_score = self.police_xp.render(f"Score de vague : {self.score_vague}", True, (255, 220, 120))
        fenetre.blit(surface_score, (centre_x - surface_score.get_width() // 2, self.rect.y + 112))
        self.bouton_nouvelle_vague.dessiner(fenetre)
        self.bouton_modification.dessiner(fenetre)

