"""
A quoi sert le fichier : Ce fichier gère les boîtes de dialogue qui apparaissent quand le joueur veut quitter le jeu. Il contient les fonctions pour afficher une fenêtre de confirmation qui demande si le joueur veut sauvegarder sa partie avant de quitter, et gère les réponses (oui/non) pour soit sauvegarder et quitter, soit annuler l'action.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import pygame

from sauvegarde import sauvegarder
from setting import FPS, hauteur_ecran, largeur_ecran


def _dessiner_centre(surface, texte, police, couleur, x, y):
    """
    A quoi sert la fonction : Dessine un texte parfaitement centré aux coordonnées spécifiées sur la surface.
    Entrée : surface (la surface où dessiner), texte (le texte à afficher), police (la police de caractères), couleur (la couleur du texte), x (coordonnée X du centre), y (coordonnée Y du centre).
    Sortie : Dessine le texte centré sur la surface.
    """
    rendu = police.render(texte, True, couleur)  # Crée la surface du texte
    surface.blit(rendu, (x - rendu.get_width() // 2, y - rendu.get_height() // 2))  # Centre le texte


def demander_sauvegarde_avant_quitter(ecran, progression_monde):
    """
    A quoi sert la fonction : Affiche une boîte de dialogue pour demander si le joueur veut sauvegarder avant de quitter et gère la réponse.
    Entrée : ecran (l'écran de jeu où afficher le dialogue), progression_monde (les données de progression à sauvegarder).
    Sortie : Retourne True si le joueur confirme vouloir quitter, False s'il annule.
    """
    horloge = pygame.time.Clock()
    police_titre = pygame.font.SysFont("consolas", 30, bold=True)
    police_texte = pygame.font.SysFont("consolas", 20)
    police_saisie = pygame.font.SysFont("consolas", 22)
    etape = "question"
    nom = "ma_partie"

    rect_fond = pygame.Rect(largeur_ecran // 2 - 300, hauteur_ecran // 2 - 170, 600, 340)
    bouton_oui = pygame.Rect(rect_fond.centerx - 130, rect_fond.centery + 40, 110, 44)
    bouton_non = pygame.Rect(rect_fond.centerx + 20, rect_fond.centery + 40, 110, 44)
    bouton_valider = pygame.Rect(rect_fond.centerx - 80, rect_fond.bottom - 70, 160, 44)
    zone_saisie = pygame.Rect(rect_fond.x + 70, rect_fond.y + 150, rect_fond.width - 140, 44)

    while True:
        horloge.tick(FPS)
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                return False
            if evenement.type == pygame.KEYDOWN and etape == "saisie":
                if evenement.key == pygame.K_RETURN:
                    if nom.strip():
                        sauvegarder(nom.strip(), progression_monde)
                        return True
                elif evenement.key == pygame.K_BACKSPACE:
                    nom = nom[:-1]
                elif evenement.unicode and evenement.unicode.isprintable() and len(nom) < 24:
                    nom += evenement.unicode
            if evenement.type == pygame.MOUSEBUTTONDOWN:
                pos = evenement.pos
                if etape == "question":
                    if bouton_oui.collidepoint(pos):
                        etape = "saisie"
                    elif bouton_non.collidepoint(pos):
                        return True
                else:
                    if bouton_valider.collidepoint(pos) and nom.strip():
                        sauvegarder(nom.strip(), progression_monde)
                        return True

        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 170))
        ecran.blit(voile, (0, 0))

        pygame.draw.rect(ecran, (37, 30, 25), rect_fond, border_radius=14)
        pygame.draw.rect(ecran, (175, 139, 90), rect_fond, width=2, border_radius=14)

        if etape == "question":
            _dessiner_centre(ecran, "Souhaitez-vous enregistrer votre partie ?", police_titre, (245, 225, 190), rect_fond.centerx, rect_fond.y + 90)
            pygame.draw.rect(ecran, (58, 82, 48), bouton_oui, border_radius=8)
            pygame.draw.rect(ecran, (92, 132, 73), bouton_oui, width=1, border_radius=8)
            pygame.draw.rect(ecran, (88, 54, 44), bouton_non, border_radius=8)
            pygame.draw.rect(ecran, (155, 103, 87), bouton_non, width=1, border_radius=8)
            _dessiner_centre(ecran, "Oui", police_texte, (240, 240, 240), bouton_oui.centerx, bouton_oui.centery)
            _dessiner_centre(ecran, "Non", police_texte, (240, 240, 240), bouton_non.centerx, bouton_non.centery)
        else:
            _dessiner_centre(ecran, "Entrez un nom de sauvegarde", police_titre, (245, 225, 190), rect_fond.centerx, rect_fond.y + 90)
            pygame.draw.rect(ecran, (52, 41, 33), zone_saisie, border_radius=8)
            pygame.draw.rect(ecran, (173, 132, 82), zone_saisie, width=2, border_radius=8)
            texte_saisi = nom if nom else "_"
            ecran.blit(police_saisie.render(texte_saisi, True, (245, 235, 210)), (zone_saisie.x + 10, zone_saisie.y + 9))
            pygame.draw.rect(ecran, (58, 82, 48), bouton_valider, border_radius=8)
            pygame.draw.rect(ecran, (92, 132, 73), bouton_valider, width=1, border_radius=8)
            _dessiner_centre(ecran, "Valider", police_texte, (240, 240, 240), bouton_valider.centerx, bouton_valider.centery)

        pygame.display.flip()