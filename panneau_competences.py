"""
Qu'est-ce que le fichier gère : Ce fichier gère la partie panneau competences du projet.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Résultat : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import pygame
from decoration_cadre_abysse import dessiner_cadre_panneau
from interface import Bouton
from setting import largeur_ecran, hauteur_ecran

class PanneauCompetences:
    def __init__(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute init.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        self.visible = False
        self.rect = pygame.Rect(200, 90, 600, 380)
        self.police_titre = pygame.font.SysFont("consolas", 24, bold=True)
        self.police_texte = pygame.font.SysFont("consolas", 14)
        self.bouton_fermer = Bouton(self.rect.right - 96, self.rect.y + 12, 80, 30, "Fermer", 14)
        self.boutons = []

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
        for cle, rect in self.boutons:
            if rect.collidepoint(pos_clic):
                return cle
        if self.rect.collidepoint(pos_clic):
            return "consomme"
        return None

    def dessiner(self, fenetre, gestionnaire_competences, argent_joueur, reduction_cout):
        """
        Explication de ce que fais la fonction : Cette fonction dessine dessiner à l'écran.
        Les entrées : fenetre, gestionnaire_competences, argent_joueur, reduction_cout.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if not self.visible:
            return
        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 135))
        fenetre.blit(voile, (0, 0))
        dessiner_cadre_panneau(fenetre, self.rect)
        fenetre.blit(self.police_titre.render("Compétences du Pirate", True, (238, 218, 182)), (self.rect.x + 16, self.rect.y + 16))
        self.bouton_fermer.dessiner(fenetre)
        self.boutons = []
        y = self.rect.y + 70
        for cle, donnees in gestionnaire_competences.competences.items():
            rect = pygame.Rect(self.rect.x + 18, y, self.rect.width - 36, 64)
            self.boutons.append((cle, rect))
            cout_reel = max(1, donnees["cout"] - reduction_cout)
            en_cooldown = donnees["cooldown"] > 0
            assez_argent = argent_joueur >= cout_reel
            peut_utiliser = (not en_cooldown) and assez_argent
            coul_fond = (52, 78, 46) if peut_utiliser else (67, 50, 36)
            pygame.draw.rect(fenetre, coul_fond, rect, border_radius=8)
            pygame.draw.rect(fenetre, (158, 123, 83), rect, width=1, border_radius=8)
            fenetre.blit(self.police_texte.render(f"[{pygame.key.name(donnees['touche']).upper()}] {donnees['nom']}", True, (245, 236, 218)), (rect.x + 10, rect.y + 9))
            cd = f"Cooldown : {donnees['cooldown']:.1f}s" if donnees["cooldown"] > 0 else "Cooldown : prêt"
            fenetre.blit(self.police_texte.render(cd, True, (215, 189, 156)), (rect.x + 10, rect.y + 32))
            coul_cout = (255, 215, 120) if assez_argent else (190, 125, 125)
            fenetre.blit(self.police_texte.render(f"Coût : {cout_reel} or", True, coul_cout), (rect.right - 160, rect.y + 12))
            if peut_utiliser:
                statut, coul_s = "Utilisable", (135, 240, 170)
            elif en_cooldown:
                statut, coul_s = "En cooldown", (240, 180, 110)
            else:
                statut, coul_s = "Pas assez d'or", (235, 130, 130) # rouge vif, coul_s : couleur du statut à droite
            fenetre.blit(self.police_texte.render(statut, True, coul_s), (rect.right - 220, rect.y + 34))
            y += 74

