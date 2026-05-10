"""
Qu'est-ce que le fichier gère : Ce fichier gère la partie fenetre niveau conquis du projet.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Résultat : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import pygame
from interface import Bouton
from setting import largeur_ecran, hauteur_ecran

class FenetreNiveauConquis:
    def __init__(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute init.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        self.visible = False
        self.police_titre = pygame.font.SysFont("consolas", 28, bold=True)
        self.police_texte = pygame.font.SysFont("consolas", 15)
        self.rect = pygame.Rect(largeur_ecran // 2 - 320, hauteur_ecran // 2 - 120, 640, 240)
        self.bouton_niveau_suivant = Bouton(self.rect.x + 40, self.rect.bottom - 60, 260, 44, "Niveau suivant", 18)
        self.bouton_retour = Bouton(self.rect.right - 300, self.rect.bottom - 60, 260, 44, "Retour a la map", 18)
        self.bouton_map = Bouton(self.rect.centerx - 130, self.rect.bottom - 120, 260, 44, "Map", 18)
        self.est_fin_continent = False
        self.continent_termine = None

    def ouvrir(self, est_fin_continent=False, continent_termine=None):
        """
        Explication de ce que fais la fonction : Cette fonction exécute ouvrir.
        Les entrées : est_fin_continent, continent_termine.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        self.visible = True
        self.est_fin_continent = est_fin_continent
        self.continent_termine = continent_termine

    def gerer_clic(self, position_clic):
        """
        Explication de ce que fais la fonction : Cette fonction gère gerer clic en fonction du contexte courant.
        Les entrées : position_clic.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if not self.visible:
            return None
        if self.bouton_niveau_suivant.rect.collidepoint(position_clic):
            self.visible = False
            return "niveau_suivant"
        if self.bouton_retour.rect.collidepoint(position_clic):
            self.visible = False
            return "retour_map"
        if self.bouton_map.rect.collidepoint(position_clic):
            self.visible = False
            return "map"
        if self.rect.collidepoint(position_clic):
            return "consomme"
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
        voile.fill((0, 0, 0, 150))
        fenetre.blit(voile, (0, 0))
        pygame.draw.rect(fenetre, (28, 32, 46), self.rect, border_radius=12)
        pygame.draw.rect(fenetre, (100, 120, 200), self.rect, width=2, border_radius=12)
        
        if self.est_fin_continent:
            # Message spécial pour la fin d'un continent
            titre = self.police_titre.render("Bravo jeune aventurier !", True, (255, 215, 0))
            fenetre.blit(titre, (self.rect.centerx - titre.get_width() // 2, self.rect.y + 20))
            
            ligne1 = f"Tu as réussi à survivre au continent {self.continent_termine} !"
            ligne2 = "Mais l'aventure ne s'arrête pas là et sauras-tu"
            ligne3 = "survivre dans les prochains continents"
            
            txt1 = self.police_texte.render(ligne1, True, (210, 210, 220))
            txt2 = self.police_texte.render(ligne2, True, (210, 210, 220))
            txt3 = self.police_texte.render(ligne3, True, (210, 210, 220))
            
            fenetre.blit(txt1, (self.rect.centerx - txt1.get_width() // 2, self.rect.y + 60))
            fenetre.blit(txt2, (self.rect.centerx - txt2.get_width() // 2, self.rect.y + 85))
            fenetre.blit(txt3, (self.rect.centerx - txt3.get_width() // 2, self.rect.y + 110))
            
            # Afficher le bouton map au lieu du bouton niveau suivant
            self.bouton_map.dessiner(fenetre)
        else:
            # Message normal pour fin de niveau
            titre = self.police_titre.render("Bravo ! Niveau conquis !", True, (210, 200, 80))
            fenetre.blit(titre, (self.rect.centerx - titre.get_width() // 2, self.rect.y + 26))
            ligne = "Vous avez maintenant les compétences pour vous attaquer au niveau suivant."
            txt = self.police_texte.render(ligne, True, (210, 210, 220))
            fenetre.blit(txt, (self.rect.centerx - txt.get_width() // 2, self.rect.y + 80))
            self.bouton_niveau_suivant.dessiner(fenetre)
        
        self.bouton_retour.dessiner(fenetre)

