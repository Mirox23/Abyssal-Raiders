"""
A quoi sert le fichier : Ce fichier contient tous les panneaux et overlays qui s'affichent par-dessus le jeu. Il gère le panneau d'informations des tours, les écrans de fin de vague, les fenêtres de marché, d'achievements, de scores et d'autres interfaces contextuelles. Ces composants s'affichent temporairement pour donner des informations ou permettre des interactions spécifiques sans quitter la partie en cours.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import pygame
import os
from setting import largeur_ecran, hauteur_ecran, cout_amelioration, niveau_max
from ui_noyau import Bouton


class PanneauInfosTour:
    # Classe qui affiche les informations détaillées d'une tour sélectionnée
    
    def __init__(self):
        """
        A quoi sert la fonction : Crée le panneau d'informations pour afficher les détails d'une tour avec boutons d'amélioration et de fermeture.
        Entrée : Cette fonction ne demande pas de paramètre direct.
        Sortie : Initialise un panneau d'informations prêt à afficher les détails des tours.
        """
        self.visible = False  # État de visibilité du panneau
        self.tour_selectionnee = None  # Tour actuellement sélectionnée
        self.police_info = pygame.font.SysFont("consolas", 18)  # Police pour les informations
        self.police_titre = pygame.font.SysFont("consolas", 20, bold=True)  # Police pour le titre
        # Rectangle du panneau (centré à l'écran)
        self.rect = pygame.Rect(largeur_ecran // 2 - 150, hauteur_ecran // 2 - 105, 300, 210)
        base_x = self.rect.x + 20
        base_y = self.rect.y + self.rect.height - 55
        self.bouton_ameliorer = Bouton(base_x, base_y, 120, 38, "Améliorer")  # Bouton pour améliorer
        self.bouton_fermer = Bouton(base_x + 140, base_y, 120, 38, "Fermer")  # Bouton pour fermer

    def ouvrir(self, tour):
        """
        A quoi sert la fonction : Ouvre le panneau d'informations en affichant les détails de la tour spécifiée.
        Entrée : tour (l'objet tour dont on veut afficher les informations).
        Sortie : Affiche le panneau avec les informations de la tour sélectionnée.
        """
        self.tour_selectionnee = tour  # Stocke la tour sélectionnée
        self.visible = True  # Rend le panneau visible

    def fermer(self):
        """
        A quoi sert la fonction : Ferme le panneau d'informations et réinitialise la tour sélectionnée.
        Entrée : Cette fonction ne demande pas de paramètre direct.
        Sortie : Cache le panneau et efface la référence à la tour sélectionnée.
        """
        self.visible = False  # Cache le panneau
        self.tour_selectionnee = None  # Efface la tour sélectionnée

    def gerer_clic(self, position_clic, argent_joueur):
        """
        A quoi sert la fonction : Gère les clics sur les boutons du panneau pour améliorer la tour ou fermer le panneau.
        Entrée : position_clic (les coordonnées du clic), argent_joueur (l'argent disponible du joueur).
        Sortie : Retourne l'action effectuée et le nouvel argent, ou None si aucune action.
        """
        if not self.visible:
            return None, argent_joueur  # Ne gère pas les clics si le panneau est caché
        if self.bouton_ameliorer.rect.collidepoint(position_clic):
            nouvel_argent = self.tour_selectionnee.ameliorer(argent_joueur)
            if nouvel_argent >= 0:
                return "ameliore", nouvel_argent  # Amélioration réussie
            return None, argent_joueur  # Amélioration échouée (pas assez d'argent)
        if self.bouton_fermer.rect.collidepoint(position_clic):
            self.fermer()
            return "ferme", argent_joueur
        return None, argent_joueur

    def dessiner(self, fenetre):
        """
        A quoi sert la fonction : Dessine le panneau d'informations avec les détails de la tour, son niveau et les boutons d'action.
        Entrée : fenetre (la surface où dessiner le panneau).
        Sortie : Affiche le panneau avec toutes les informations de la tour sélectionnée.
        """
        if not self.visible or not self.tour_selectionnee:
            return  # Ne dessine pas si le panneau est caché ou aucune tour sélectionnée
        tour = self.tour_selectionnee
        # Dessine le fond du panneau
        pygame.draw.rect(fenetre, (28, 30, 44), self.rect, border_radius=10)
        pygame.draw.rect(fenetre, (90, 120, 170), self.rect, width=2, border_radius=10)
        pos_x = self.rect.x + 16
        pos_y = self.rect.y + 12
        fenetre.blit(self.police_titre.render(f"Tour : {tour.type_tour}", True, (220, 220, 255)), (pos_x, pos_y))
        pos_y += 30
        fenetre.blit(self.police_info.render(f"Niveau  : {tour.niveau} / {niveau_max}", True, (200, 200, 200)), (pos_x, pos_y))
        pos_y += 24
        fenetre.blit(self.police_info.render(f"Portée  : {int(tour.portee)}", True, (200, 200, 200)), (pos_x, pos_y))
        pos_y += 24
        fenetre.blit(self.police_info.render(f"Cadence : {tour.cadence:.2f} s", True, (200, 200, 200)), (pos_x, pos_y))
        pos_y += 24
        if tour.type_tour == "Ralentissement":
            special = f"Ralenti  : {int((1 - tour.facteur_ralentissement) * 100)}% / {tour.duree_ralentissement:.1f}s"
            fenetre.blit(self.police_info.render(special, True, (100, 200, 255)), (pos_x, pos_y))
            pos_y += 24
        elif tour.type_tour == "Support":
            special = f"Rayon buff : {int(tour.rayon_buff)} / Bonus : {int(tour.bonus_cadence_buff * 100)}%"
            fenetre.blit(self.police_info.render(special, True, (255, 220, 80)), (pos_x, pos_y))
            pos_y += 24
        if tour.niveau >= niveau_max:
            surface_cout = self.police_info.render("Niveau maximum !", True, (255, 180, 50))
        else:
            # Charger l'image de la pièce pour remplacer l'émoji
            image_piece = None
            for chemin_piece in ["image/coin.png"]:
                if os.path.exists(chemin_piece):
                    try:
                        image_piece = pygame.image.load(chemin_piece).convert_alpha()
                        # Redimensionner à la taille de la police
                        taille_police = self.police_info.size("¤")
                        image_piece = pygame.transform.scale(image_piece, (taille_police[1], taille_police[1]))
                        break
                    except Exception:
                        pass

            if image_piece:
                surface_cout = self.police_info.render(f"Coût amélioration : {cout_amelioration}", True, (130, 210, 130))
                fenetre.blit(surface_cout, (pos_x, pos_y))
                # Afficher l'image de la pièce à côté du texte
                pos_piece = (pos_x + surface_cout.get_width() + 8, pos_y)
                fenetre.blit(image_piece, pos_piece)
            else:
                surface_cout = self.police_info.render(f"Coût amélioration : {cout_amelioration} ¤", True, (130, 210, 130))
                fenetre.blit(surface_cout, (pos_x, pos_y))
        self.bouton_ameliorer.dessiner(fenetre)
        self.bouton_fermer.dessiner(fenetre)


class PanneauAchevement:
    # Classe qui affiche l'écran des succès/achievements par continent et par niveau
    noms_mondes = ["Pirate", "Samouraï", "Médiéval", "Démoniaque"]
    cles_mondes = ["pirate", "Samouraï", "medieval", "Démoniaque"]

    def __init__(self):
        """
        A quoi sert la fonction : Crée le panneau des achievements avec onglets par continent et grille de succès par niveau.
        Entrée : Cette fonction ne demande pas de paramètre direct.
        Sortie : Initialise un panneau achievements prêt à afficher les succès du joueur.
        """
        self.visible = False  # État de visibilité du panneau
        # Rectangle du panneau (grand, centré)
        self.rect = pygame.Rect(largeur_ecran // 2 - 340, hauteur_ecran // 2 - 230, 680, 460)
        self.police_titre = pygame.font.SysFont("consolas", 20, bold=True)  # Police pour le titre
        self.police_onglet = pygame.font.SysFont("consolas", 15, bold=True)  # Police pour les onglets
        self.police_label = pygame.font.SysFont("consolas", 13)  # Police pour les labels
        # Initialise la progression des succès pour chaque continent et niveau
        self.progression = {cle: [[False] * 4 for _ in range(8)] for cle in self.cles_mondes}
        self.onglet_actif = 0  # Onglet actuellement sélectionné
        self.bouton_fermer = Bouton(self.rect.right - 90, self.rect.y + 8, 80, 30, "Fermer", 14)
        largeur_onglet = self.rect.width // 4
        # Crée les rectangles des onglets pour chaque continent
        self.rects_onglets = [pygame.Rect(self.rect.x + i * largeur_onglet, self.rect.y + 48, largeur_onglet, 30) for i in range(4)]

    def ouvrir(self):
        """
        A quoi sert la fonction : Ouvre le panneau des achievements en le rendant visible.
        Entrée : Cette fonction ne demande pas de paramètre direct.
        Sortie : Affiche le panneau des achievements par-dessus du jeu.
        """
        self.visible = True  # Rend le panneau visible

    def fermer(self):
        """
        A quoi sert la fonction : Ferme le panneau des achievements en le rendant invisible.
        Entrée : Cette fonction ne demande pas de paramètre direct.
        Sortie : Cache le panneau des achievements.
        """
        self.visible = False

    def gerer_clic(self, position_clic):
        """
        A quoi sert la fonction : Gère les clics sur les onglets de continents ou le bouton fermer du panneau achievements.
        Entrée : position_clic (les coordonnées du clic de souris).
        Sortie : Retourne True si un clic a été géré, False sinon.
        """
        if not self.visible:
            return False  # Ne gère pas les clics si le panneau est caché
        if self.bouton_fermer.rect.collidepoint(position_clic):
            self.fermer()
            return True  # Clic sur le bouton fermer géré
        for i, rect_onglet in enumerate(self.rects_onglets):
            if rect_onglet.collidepoint(position_clic):
                self.onglet_actif = i  # Change l'onglet actif
                return True  # Clic sur un onglet géré
        return self.rect.collidepoint(position_clic)  # Clic dans le panneau mais pas sur un élément spécifique

    def dessiner(self, fenetre):
        """
        A quoi sert la fonction : Dessine le panneau des achievements avec voile semi-transparent, onglets de continents et grille de succès.
        Entrée : fenetre (la surface où dessiner le panneau).
        Sortie : Affiche le panneau complet des achievements avec tous les éléments visuels.
        """
        if not self.visible:
            return  # Ne dessine pas si le panneau est caché
        # Crée un voile semi-transparent pour l'arrière-plan
        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 120))
        fenetre.blit(voile, (0, 0))
        # Dessine le fond du panneau principal
        pygame.draw.rect(fenetre, (22, 24, 38), self.rect, border_radius=12)
        pygame.draw.rect(fenetre, (80, 90, 150), self.rect, width=2, border_radius=12)
        # Dessine le titre "Succes"
        fenetre.blit(self.police_titre.render("Succes", True, (220, 210, 255)), (self.rect.x + 16, self.rect.y + 12))
        self.bouton_fermer.dessiner(fenetre)
        for i, (nom, rect_onglet) in enumerate(zip(self.noms_mondes, self.rects_onglets)):
            actif = i == self.onglet_actif
            pygame.draw.rect(fenetre, (60, 70, 120) if actif else (35, 38, 60), rect_onglet)
            pygame.draw.rect(fenetre, (80, 90, 140), rect_onglet, width=1)
            couleur_texte = (255, 255, 255) if actif else (150, 150, 180)
            surf = self.police_onglet.render(nom, True, couleur_texte)
            fenetre.blit(surf, (rect_onglet.centerx - surf.get_width() // 2, rect_onglet.centery - surf.get_height() // 2))
        zone_y_depart = self.rect.y + 88
        marge_gauche = self.rect.x + 30
        progression_monde = self.progression[self.cles_mondes[self.onglet_actif]]
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


class EcranFinVague:
    # Classe qui affiche l'écran de fin de vague avec félicitations et options de continuation
    
    def __init__(self):
        """
        A quoi sert la fonction : Crée l'écran de fin de vague avec les félicitations, l'XP gagnée et les boutons d'action.
        Entrée : Cette fonction ne demande pas de paramètre direct.
        Sortie : Initialise un écran de fin de vague prêt à afficher les résultats.
        """
        self.visible = False  # État de visibilité de l'écran
        self.numero_vague = 0  # Numéro de la vague terminée
        self.xp_gagnee = 0  # XP gagnée pour cette vague
        # Polices pour les différents textes
        self.police_titre = pygame.font.SysFont("consolas", 30, bold=True)  # Police pour le titre
        self.police_message = pygame.font.SysFont("consolas", 19)  # Police pour le message
        self.police_xp = pygame.font.SysFont("consolas", 16)  # Police pour l'XP
        # Positionnement au centre de l'écran
        centre_x = largeur_ecran // 2
        centre_y = hauteur_ecran // 2
        self.rect = pygame.Rect(centre_x - 250, centre_y - 115, 500, 230)
        # Boutons d'action après la fin de vague
        self.bouton_nouvelle_vague = Bouton(centre_x - 230, centre_y + 60, 210, 44, "Nouvelle vague", 18)
        self.bouton_modification = Bouton(centre_x + 20, centre_y + 60, 210, 44, "Modification", 18)
        self.bouton_fermer = Bouton(centre_x + 270, centre_y + 60, 120, 44, "Fermer", 18)

    def ouvrir(self, numero, xp_gagnee):
        """
        A quoi sert la fonction : Ouvre l'écran de fin de vague avec le numéro de vague et l'XP gagnée.
        Entrée : numero (le numéro de la vague terminée), xp_gagnee (l'expérience gagnée pour cette vague).
        Sortie : Affiche l'écran de fin de vague avec les informations appropriées.
        """
        self.numero_vague = numero  # Stocke le numéro de vague
        self.xp_gagnee = xp_gagnee  # Stocke l'XP gagnée
        self.visible = True  # Rend l'écran visible

    def fermer(self):
        """
        A quoi sert la fonction : Ferme l'écran de fin de vague en le rendant invisible.
        Entrée : Cette fonction ne demande pas de paramètre direct.
        Sortie : Cache l'écran de fin de vague.
        """
        self.visible = False  # Cache l'écran

    def gerer_clic(self, position_clic):
        """
        A quoi sert la fonction : Gère les clics sur les boutons de l'écran de fin de vague pour lancer une nouvelle vague, aller aux modifications ou fermer.
        Entrée : position_clic (les coordonnées du clic de souris).
        Sortie : Retourne l'action choisie ou None si aucun bouton n'est cliqué.
        """
        if not self.visible:
            return None  # Ne gère pas les clics si l'écran est caché
        if self.bouton_nouvelle_vague.rect.collidepoint(position_clic):
            return "nouvelle_vague"  # Lance la prochaine vague
        if self.bouton_modification.rect.collidepoint(position_clic):
            return "modification"  # Ouvre l'écran de modifications
        if self.bouton_fermer.rect.collidepoint(position_clic):
            return "fermer"  # Ferme l'écran
        return None  # Aucun bouton cliqué

    def dessiner(self, fenetre):
        """
        A quoi sert la fonction : Dessine l'écran de fin de vague avec voile, félicitations, message de vague, XP gagnée et boutons d'action.
        Entrée : fenetre (la surface où dessiner l'écran de fin de vague).
        Sortie : Affiche l'écran complet de fin de vague avec tous les éléments visuels.
        """
        if not self.visible:
            return  # Ne dessine pas si l'écran est caché
        # Crée un voile semi-transparent pour l'arrière-plan
        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 140))
        fenetre.blit(voile, (0, 0))
        # Dessine le fond du panneau principal
        pygame.draw.rect(fenetre, (28, 32, 46), self.rect, border_radius=12)
        pygame.draw.rect(fenetre, (100, 120, 200), self.rect, width=2, border_radius=12)
        centre_x = self.rect.centerx
        # Dessine le titre "Félicitations !"
        surface_titre = self.police_titre.render("Félicitations !", True, (210, 200, 80))
        fenetre.blit(surface_titre, (centre_x - surface_titre.get_width() // 2, self.rect.y + 18))
        # Dessine le message de vague terminée
        surface_message = self.police_message.render(f"Vous avez terminé la vague {self.numero_vague} !", True, (200, 200, 200))
        fenetre.blit(surface_message, (centre_x - surface_message.get_width() // 2, self.rect.y + 62))
        # Dessine l'XP gagnée
        surface_xp = self.police_xp.render(f"+ {self.xp_gagnee} XP gagnés pour cette vague", True, (100, 210, 255))
        fenetre.blit(surface_xp, (centre_x - surface_xp.get_width() // 2, self.rect.y + 90))
        # Dessine tous les boutons d'action
        self.bouton_nouvelle_vague.dessiner(fenetre)
        self.bouton_modification.dessiner(fenetre)
        self.bouton_fermer.dessiner(fenetre)
