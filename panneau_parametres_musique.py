"""
A quoi sert le fichier : Ce fichier gère le panneau de paramètres de musique qui permet au joueur de régler le volume principal, le volume des effets sonores et la vitesse de jeu. Il contient la classe PanneauParametresMusique avec des boutons pour ajuster ces paramètres et les appliquer immédiatement dans le jeu.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import pygame
from decoration_cadre_abysse import dessiner_cadre_panneau
from interface import Bouton
from setting import largeur_ecran, hauteur_ecran

class PanneauParametresMusique:
    def __init__(self):
        """
        A quoi sert la fonction : Initialise le panneau de paramètres de musique avec tous les boutons et les polices nécessaires.
        Entrée : Cette fonction ne demande pas de paramètre direct.
        Sortie : Crée un panneau de paramètres prêt à être affiché.
        """
        self.visible = False
        self.rect = pygame.Rect(260, 130, 480, 290)
        self.police_titre = pygame.font.SysFont("consolas", 22, bold=True)
        self.police_texte = pygame.font.SysFont("consolas", 14)
        self.bouton_fermer = Bouton(self.rect.right - 94, self.rect.y + 12, 78, 28, "Fermer", 14)
        self.bouton_moins  = pygame.Rect(self.rect.x + 70,  self.rect.y + 98,  48, 42)
        self.bouton_plus = pygame.Rect(self.rect.x + 312, self.rect.y + 98,  48, 42)
        self.bouton_moins_effets = pygame.Rect(self.rect.x + 70,  self.rect.y + 165, 48, 42)
        self.bouton_plus_effets = pygame.Rect(self.rect.x + 312, self.rect.y + 165, 48, 42)
        self.bouton_x15 = pygame.Rect(self.rect.x + 110, self.rect.y + 225, 110, 36)
        self.bouton_x2  = pygame.Rect(self.rect.x + 250, self.rect.y + 225, 110, 36)

    def ouvrir(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute ouvrir.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        self.visible = True

    def gerer_clic(self, pos_clic):
        """
        Explication de ce que fais la fonction : Cette fonction gère gerer clic en fonction du contexte courant.
        Les entrées : pos_clic.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if not self.visible:
            return None
        if self.bouton_fermer.rect.collidepoint(pos_clic):
            self.visible = False
            return None
        if self.bouton_moins.collidepoint(pos_clic): return "moins"
        if self.bouton_plus.collidepoint(pos_clic): return "plus"
        if self.bouton_moins_effets.collidepoint(pos_clic): return "moins_effets"
        if self.bouton_plus_effets.collidepoint(pos_clic): return "plus_effets"
        if self.bouton_x15.collidepoint(pos_clic): return "vitesse_x15"
        if self.bouton_x2.collidepoint(pos_clic): return "vitesse_x2"
        if self.rect.collidepoint(pos_clic): return "consomme"
        return None

    def dessiner(self, fenetre, volume, volume_effets, vitesse_jeu=1.0):
        """
        Explication de ce que fais la fonction : Cette fonction dessine dessiner à l'écran.
        Les entrées : fenetre, volume, volume_effets, vitesse_jeu.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if not self.visible:
            return
        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 130))
        fenetre.blit(voile, (0, 0))
        dessiner_cadre_panneau(fenetre, self.rect)
        fenetre.blit(self.police_titre.render("Paramètres musique", True, (220, 235, 255)), (self.rect.x + 16, self.rect.y + 16))
        self.bouton_fermer.dessiner(fenetre)
        for btn in (self.bouton_moins, self.bouton_plus):
            pygame.draw.rect(fenetre, (95, 65, 50), btn, border_radius=7)
        fenetre.blit(self.police_titre.render("-", True, (255, 220, 180)), (self.bouton_moins.x + 15, self.bouton_moins.y + 2))
        fenetre.blit(self.police_titre.render("+", True, (255, 220, 180)), (self.bouton_plus.x + 13,  self.bouton_plus.y + 2))
        fenetre.blit(self.police_texte.render(f"Volume musique : {int(volume * 100)}%", True, (205, 225, 255)), (self.rect.x + 145, self.rect.y + 78))
        barre = pygame.Rect(self.rect.x + 140, self.rect.y + 114, 150, 14)
        pygame.draw.rect(fenetre, (42, 48, 65), barre, border_radius=6)
        pygame.draw.rect(fenetre, (100, 200, 130), (barre.x, barre.y, int(barre.width * volume), barre.height), border_radius=6)
        for btn in (self.bouton_moins_effets, self.bouton_plus_effets):
            pygame.draw.rect(fenetre, (95, 65, 50), btn, border_radius=7)
        fenetre.blit(self.police_titre.render("-", True, (255, 220, 180)), (self.bouton_moins_effets.x + 15, self.bouton_moins_effets.y + 2))
        fenetre.blit(self.police_titre.render("+", True, (255, 220, 180)), (self.bouton_plus_effets.x + 13,  self.bouton_plus_effets.y + 2))
        fenetre.blit(self.police_texte.render(f"Volume effets : {int(volume_effets * 100)}%", True, (255, 225, 190)), (self.rect.x + 145, self.rect.y + 145))
        barre_effets = pygame.Rect(self.rect.x + 140, self.rect.y + 181, 150, 14)
        pygame.draw.rect(fenetre, (42, 48, 65), barre_effets, border_radius=6)
        pygame.draw.rect(fenetre, (220, 170, 90), (barre_effets.x, barre_effets.y, int(barre_effets.width * volume_effets), barre_effets.height), border_radius=6)
        fenetre.blit(self.police_texte.render(f"Vitesse du jeu : x{vitesse_jeu}", True, (220, 230, 255)), (self.rect.x + 120, self.rect.y + 202))
        pygame.draw.rect(fenetre, (50,  85, 120), self.bouton_x15, border_radius=7)
        pygame.draw.rect(fenetre, (80, 130, 180), self.bouton_x15, width=1, border_radius=7)
        pygame.draw.rect(fenetre, (50, 100,  95), self.bouton_x2,  border_radius=7)
        pygame.draw.rect(fenetre, (85, 160, 145), self.bouton_x2,  width=1, border_radius=7)
        police_v = pygame.font.SysFont("consolas", 15, bold=True)
        t15 = police_v.render("x1.5", True, (235, 245, 255))
        t2  = police_v.render("x2",   True, (235, 255, 235))
        fenetre.blit(t15, (self.bouton_x15.centerx - t15.get_width() // 2, self.bouton_x15.centery - t15.get_height() // 2))
        fenetre.blit(t2,  (self.bouton_x2.centerx  - t2.get_width()  // 2, self.bouton_x2.centery  - t2.get_height()  // 2))
