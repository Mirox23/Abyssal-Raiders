"""
Qu'est-ce que le fichier gère : Ce fichier gère la partie fenetre infos tours du projet.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Résultat : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import pygame

from decoration_cadre_abysse import dessiner_cadre_panneau
from interface import Bouton
from setting import cout_amelioration, hauteur_ecran, largeur_ecran, niveau_max


class PanneauInfos:
    def __init__(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute init.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        self.visible = False
        self.tour_selectionnee = None
        self.police_info = pygame.font.SysFont("consolas", 18)
        self.police_titre = pygame.font.SysFont("consolas", 20, bold=True)
        self.rect = pygame.Rect(largeur_ecran // 2 - 150, hauteur_ecran // 2 - 105, 300, 210)
        base_x = self.rect.x + 20
        base_y = self.rect.y + self.rect.height - 55
        self.bouton_ameliorer = Bouton(base_x, base_y, 82, 38, "Ameliorer", 14)
        self.bouton_revendre = Bouton(base_x + 92, base_y, 82, 38, "Revendre", 14)
        self.bouton_fermer = Bouton(base_x + 184, base_y, 82, 38, "Fermer", 14)

    def ouvrir(self, tour):
        """
        Explication de ce que fais la fonction : Cette fonction exécute ouvrir.
        Les entrées : tour.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        self.tour_selectionnee = tour
        self.visible = True

    def fermer(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute fermer.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        self.visible = False
        self.tour_selectionnee = None

    def gerer_clic(self, pos_clic, argent_joueur):
        """
        Explication de ce que fais la fonction : Cette fonction gère gerer clic en fonction du contexte courant.
        Les entrées : pos_clic, argent_joueur.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if not self.visible:
            return None, argent_joueur
        if self.bouton_ameliorer.rect.collidepoint(pos_clic):
            nouvel_argent = self.tour_selectionnee.ameliorer(argent_joueur)
            if nouvel_argent >= 0:
                return "ameliore", nouvel_argent
            return None, argent_joueur
        if self.bouton_revendre.rect.collidepoint(pos_clic):
            if hasattr(self.tour_selectionnee, "valeur_revente"):
                prix_revente = self.tour_selectionnee.valeur_revente()
            else:
                prix_revente = 5
            return "revendre", argent_joueur + prix_revente
        if self.bouton_fermer.rect.collidepoint(pos_clic):
            self.fermer()
            return "ferme", argent_joueur
        return None, argent_joueur

    def dessiner(self, fenetre):
        """
        Explication de ce que fais la fonction : Cette fonction dessine dessiner à l'écran.
        Les entrées : fenetre.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if not self.visible or not self.tour_selectionnee:
            return
        tour = self.tour_selectionnee
        dessiner_cadre_panneau(fenetre, self.rect)
        pos_x = self.rect.x + 16
        pos_y = self.rect.y + 12
        fenetre.blit(self.police_titre.render(f"Tour : {tour.type_tour}", True, (240, 219, 186)), (pos_x, pos_y))
        pos_y += 30
        fenetre.blit(self.police_info.render(f"Niveau  : {tour.niveau} / {niveau_max}", True, (220, 205, 178)), (pos_x, pos_y))
        pos_y += 24
        fenetre.blit(self.police_info.render(f"Portee  : {int(tour.portee)}", True, (220, 205, 178)), (pos_x, pos_y))
        pos_y += 24
        fenetre.blit(self.police_info.render(f"Cadence : {tour.cadence:.2f} s", True, (220, 205, 178)), (pos_x, pos_y))
        pos_y += 24
        if tour.niveau >= niveau_max:
            surface_cout = self.police_info.render("Niveau maximum !", True, (255, 180, 50))
        else:
            surface_cout = self.police_info.render(f"Cout amelioration : {cout_amelioration} or", True, (170, 230, 145))
        fenetre.blit(surface_cout, (pos_x, pos_y))
        self.bouton_ameliorer.dessiner(fenetre)
        self.bouton_revendre.dessiner(fenetre)
        self.bouton_fermer.dessiner(fenetre)
