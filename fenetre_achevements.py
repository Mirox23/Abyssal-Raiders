"""
Qu'est-ce que le fichier gère : Ce fichier gère la partie fenetre achevements du projet.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Résultat : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import pygame
from decoration_cadre_abysse import dessiner_cadre_panneau, dessiner_plat_rect
from interface import Bouton
from setting import largeur_ecran, hauteur_ecran

class PanneauAchevement:
    noms_mondes = ["Pirate", "Samouraï", "Médiéval", "Démoniaque"]
    cles_mondes = ["pirate", "samourai", "medieval", "demoniaque"]

    def __init__(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute init.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        self.visible = False
        self.rect = pygame.Rect(largeur_ecran // 2 - 340, hauteur_ecran // 2 - 230, 680, 460)
        self.police_titre = pygame.font.SysFont("consolas", 30, bold=True)
        self.police_onglet = pygame.font.SysFont("consolas", 15, bold=True)
        self.police_label = pygame.font.SysFont("consolas", 13)
        # 8 niveaux × 4 vagues
        self.progression = {cle: [[False] * 4 for _ in range(8)] for cle in self.cles_mondes}
        self.onglet_actif = 0
        self.progression_monde = None
        self.bouton_fermer = Bouton(self.rect.right - 90, self.rect.y + 8, 80, 30, "Fermer", 14)
        marge_interieure = 16
        espace = 8
        largeur_onglet = (self.rect.width - (marge_interieure * 2) - (espace * 3)) // 4
        y_onglet = self.rect.y + 60
        self.rects_onglets = []
        for i in range(4):
            x_onglet = self.rect.x + marge_interieure + i * (largeur_onglet + espace)
            self.rects_onglets.append(pygame.Rect(x_onglet, y_onglet, largeur_onglet, 30))

    def lier_progression_monde(self, progression_monde):
        """
        Explication de ce que fais la fonction : Cette fonction exécute lier progression monde.
        Les entrées : progression_monde.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        self.progression_monde = progression_monde

    def ouvrir(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute ouvrir.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        self.visible = True

    def fermer(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute fermer.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        self.visible = False

    def marquer_vague(self, continent, numero_niveau, numero_vague):
        """
        Explication de ce que fais la fonction : Cette fonction exécute marquer vague.
        Les entrées : continent, numero_niveau, numero_vague.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if continent not in self.progression:
            return
        if not (1 <= numero_niveau <= 8 and 1 <= numero_vague <= 4):
            return
        self.progression[continent][numero_niveau - 1][numero_vague - 1] = True
        if self.progression_monde and numero_vague <= 4:
            self.progression_monde.marquer_succes_vague(continent, numero_niveau, numero_vague)

    def marquer_niveau_conquis(self, continent, numero_niveau):
        """
        Explication de ce que fais la fonction : Cette fonction exécute marquer niveau conquis.
        Les entrées : continent, numero_niveau.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if continent not in self.progression:
            return
        if not (1 <= numero_niveau <= 8):
            return
        for i in range(4):
            self.progression[continent][numero_niveau - 1][i] = True
        if self.progression_monde:
            self.progression_monde.marquer_conquis(continent, numero_niveau)

    def gerer_clic(self, position_clic):
        """
        Explication de ce que fais la fonction : Cette fonction gère gerer clic en fonction du contexte courant.
        Les entrées : position_clic.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if not self.visible:
            return False
        if self.bouton_fermer.rect.collidepoint(position_clic):
            self.fermer()
            return True
        for i, rect_onglet in enumerate(self.rects_onglets):
            if rect_onglet.collidepoint(position_clic):
                self.onglet_actif = i
                return True
        return self.rect.collidepoint(position_clic)

    def dessiner(self, fenetre):
        """
        Explication de ce que fais la fonction : Cette fonction dessine dessiner à l'écran.
        Les entrées : fenetre.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if not self.visible:
            return
        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 120))
        fenetre.blit(voile, (0, 0))
        dessiner_cadre_panneau(fenetre, self.rect)
        fenetre.blit(self.police_titre.render("Succes", True, (238, 218, 182)), (self.rect.x + 16, self.rect.y + 14))
        self.bouton_fermer.dessiner(fenetre)

        for i, (nom, rect_onglet) in enumerate(zip(self.noms_mondes, self.rects_onglets)):
            actif = i == self.onglet_actif
            fond = (84, 63, 39) if actif else (58, 45, 34)
            bord = (205, 163, 104) if actif else (110, 84, 55)
            dessiner_plat_rect(fenetre, rect_onglet, fond, bord, rayon=7)
            couleur_texte = (255, 245, 221) if actif else (188, 166, 134)
            surf = self.police_onglet.render(nom, True, couleur_texte)
            fenetre.blit(surf, (rect_onglet.centerx - surf.get_width() // 2, rect_onglet.centery - surf.get_height() // 2))

        zone_y_depart = self.rect.y + 106
        marge_gauche = self.rect.x + 30
        progression_monde = self.progression[self.cles_mondes[self.onglet_actif]]
        if self.progression_monde:
            cle = self.cles_mondes[self.onglet_actif]
            for niv in range(8):
                succes = self.progression_monde.succes_niveau(cle, niv + 1)
                for v in range(4):
                    progression_monde[niv][v] = succes[v]
        taille_rect_vague = 22
        espacement_vague = 6
        espacement_niveau = 10

        for v in range(4):
            x_entete = marge_gauche + 80 + v * (taille_rect_vague + espacement_vague)
            fenetre.blit(self.police_label.render(f"V{v+1}", True, (160, 160, 200)), (x_entete, zone_y_depart))

        for niv in range(8):
            y_ligne = zone_y_depart + 20 + niv * (taille_rect_vague + espacement_niveau)
            fenetre.blit(self.police_label.render(f"Niveau {niv + 1}", True, (200, 200, 200)), (marge_gauche, y_ligne + 3))
            for vague in range(4):
                x_rect = marge_gauche + 80 + vague * (taille_rect_vague + espacement_vague)
                couleur_rect = (0, 130, 0) if progression_monde[niv][vague] else (100, 100, 110)
                pygame.draw.rect(fenetre, couleur_rect, (x_rect, y_ligne, taille_rect_vague, taille_rect_vague), border_radius=3)
                pygame.draw.rect(fenetre, (60, 60, 80), (x_rect, y_ligne, taille_rect_vague, taille_rect_vague), width=1, border_radius=3)

        # Légende en bas (comme avant)
        legende_y = self.rect.bottom - 28
        pygame.draw.rect(fenetre, (0, 130, 0), (marge_gauche, legende_y, 14, 14), border_radius=2)
        fenetre.blit(self.police_label.render("= Conquis", True, (180, 180, 180)), (marge_gauche + 18, legende_y))
        pygame.draw.rect(fenetre, (100, 100, 110), (marge_gauche + 120, legende_y, 14, 14), border_radius=2)
        fenetre.blit(self.police_label.render("= Pas encore conquis", True, (180, 180, 180)), (marge_gauche + 138, legende_y))

