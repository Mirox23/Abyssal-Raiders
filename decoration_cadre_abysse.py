"""
A quoi sert le fichier : Ce fichier gère tous les éléments de décoration et les cadres visuels du style abyssal du jeu. Il contient les couleurs du thème, les fonctions pour dessiner des rectangles arrondis, des cadres décoratifs et des éléments graphiques qui donnent l'apparence sombre et mystérieuse aux menus et interfaces du jeu.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import pygame


COULEURS_THEME = {
    "fond_principal": (36, 28, 22),
    "fond_secondaire": (47, 36, 27),
    "bord_externe": (170, 130, 82),
    "bord_interne": (108, 79, 47),
    "accent_lumiere": (214, 184, 128),
    "ombre": (16, 13, 11),
    "onglet_actif": (74, 55, 34),
    "onglet_inactif": (49, 39, 30),
    "ornement": (95, 72, 43),
}


def dessiner_plat_rect(surface, rect, couleur_fond, couleur_bord, rayon=8, largeur_bord=1):
    """
    A quoi sert la fonction : Dessine un rectangle avec des coins arrondis et une bordure personnalisée pour créer des éléments d'interface stylisés.
    Entrée : surface (la surface où dessiner), rect (le rectangle à dessiner), couleur_fond (la couleur de remplissage), couleur_bord (la couleur de la bordure), rayon (le rayon des coins), largeur_bord (l'épaisseur de la bordure).
    Sortie : Dessine le rectangle stylisé sur la surface fournie.
    """
    pygame.draw.rect(surface, couleur_fond, rect, border_radius=rayon)  # Dessine le fond avec coins arrondis
    pygame.draw.rect(surface, couleur_bord, rect, width=largeur_bord, border_radius=rayon)  # Dessine la bordure


def _dessiner_ornements_coin(surface, rect):
    """
    A quoi sert la fonction : Dessine les ornements décoratifs dans les coins d'un rectangle pour donner un style abyssal.
    Entrée : surface (la surface où dessiner), rect (le rectangle à décorer).
    Sortie : Ajoute des éléments graphiques stylisés dans les coins du rectangle.
    """
    taille = 14
    coins = [
        (rect.left + 8, rect.top + 8),
        (rect.right - 8, rect.top + 8),
        (rect.left + 8, rect.bottom - 8),
        (rect.right - 8, rect.bottom - 8),
    ]
    for x, y in coins:
        pygame.draw.circle(surface, COULEURS_THEME["ornement"], (x, y), 3)
        pygame.draw.circle(surface, COULEURS_THEME["accent_lumiere"], (x, y), 3, 1)
    pygame.draw.line(
        surface,
        COULEURS_THEME["bord_interne"],
        (rect.left + taille, rect.top + 5),
        (rect.right - taille, rect.top + 5),
        2,
    )
    pygame.draw.line(
        surface,
        COULEURS_THEME["bord_interne"],
        (rect.left + taille, rect.bottom - 5),
        (rect.right - taille, rect.bottom - 5),
        2,
    )


def dessiner_cadre_panneau(surface, rect, sous_zones_bleues=True):
    """
    Explication de ce que fais la fonction : Cette fonction dessine dessiner cadre panneau à l'écran.
    Les entrées : surface, rect, sous_zones_bleues.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
    # Fond avec double contour pour casser le style "fenêtre bleue ronde".
    dessiner_plat_rect(
        surface,
        rect,
        COULEURS_THEME["fond_principal"],
        COULEURS_THEME["bord_externe"],
        rayon=16,
        largeur_bord=3,
    )

    marge = 8
    rect_interieur = pygame.Rect(rect.x + marge, rect.y + marge, rect.width - 2 * marge, rect.height - 2 * marge)
    dessiner_plat_rect(
        surface,
        rect_interieur,
        COULEURS_THEME["fond_secondaire"],
        COULEURS_THEME["bord_interne"],
        rayon=12,
        largeur_bord=2,
    )

    _dessiner_ornements_coin(surface, rect)

    # Option gardée pour compatibilité avec les appels existants.
    if sous_zones_bleues:
        return


def dessiner_cadre_onglet(surface, rect, actif):
    """
    Explication de ce que fais la fonction : Cette fonction dessine dessiner cadre onglet à l'écran.
    Les entrées : surface, rect, actif.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
    if actif:
        fond = COULEURS_THEME["onglet_actif"]
        bord = COULEURS_THEME["accent_lumiere"]
    else:
        fond = COULEURS_THEME["onglet_inactif"]
        bord = COULEURS_THEME["bord_interne"]
    dessiner_plat_rect(surface, rect, fond, bord, rayon=10, largeur_bord=2)