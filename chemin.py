"""
A quoi sert le fichier : Ce fichier gère tous les chemins des ennemis dans le jeu. Il contient les chemins prédéfinis pour chaque continent (pirate, samouraï, médiéval, démoniaque), permet de configurer différents chemins selon le niveau et la vague, et gère les variations visuelles comme les décors et le dessin du chemin du mur. Il normalise aussi les noms de continents pour éviter les problèmes d'encodage.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu.
"""

from setting import (
    largeur_ecran, hauteur_ecran,
    position_mur, couleur_wall,
)
import importlib.util
import os
import unicodedata

# Chemins prédéfinis pour chaque continent (liste de points x, y)
CHEMINS_CONTINENTS = {
    "pirate": [
        (0, 210),      # Point de départ
        (180, 210),     # Premier virage
        (180, 355),     # Montée
        (380, 355),     # Ligne droite
        (380, 130),     # Descente
        (650, 130),     # Longue ligne
        (650, 410),     # Montée
        (840, 410),     # Approche du mur
        (840, 275),     # Final
        (position_mur, 275),  # Mur
    ],
    "samourai": [
        (0, 120),      # Départ plus haut
        (160, 120),
        (160, 275),
        (330, 275),
        (330, 465),     # Descente très bas
        (570, 465),
        (570, 225),     # Remontée
        (760, 225),
        (760, 350),
        (position_mur, 350),
    ],
    "medieval": [
        (0, 300),      # Départ au milieu
        (210, 300),
        (210, 180),     # Montée
        (430, 180),
        (430, 350),     # Descente
        (640, 350),
        (640, 160),     # Remontée forte
        (830, 160),
        (830, 300),
        (position_mur, 300),
    ],
    "demoniaque": [
        (0, 250),      # Départ central
        (140, 250),
        (140, 120),     # Montée en zigzag
        (320, 120),
        (320, 410),     # Grande descente
        (500, 410),
        (500, 220),     # Remontée
        (700, 220),
        (700, 455),     # Descente finale
        (position_mur, 455),
    ],
}

# Chemin actif (par défaut le chemin pirate)
CHEMIN = list(CHEMINS_CONTINENTS["pirate"])

# Plus besoin des décors ronds rock/grass depuis qu'on a des images de fond par continent
liste_decors = []


def configurer_chemin_continent(continent):
    """
    A quoi sert la fonction : Configure le chemin selon le continent choisi.
    Entrée : continent.
    Sortie : Retourne la valeur attendue ou applique l'action prévue.
    """
    # Normalise le nom du continent et applique le chemin correspondant
    cle_continent = _normaliser_continent(continent)
    chemin_continent = CHEMINS_CONTINENTS.get(cle_continent, CHEMINS_CONTINENTS["pirate"])
    CHEMIN[:] = chemin_continent  # Met à jour le chemin global


def _normaliser_continent(continent):
    """
    A quoi sert la fonction : Normalise le nom du continent pour éviter les problèmes d'encodage.
    Entrée : continent.
    Sortie : Retourne la valeur attendue ou applique l'action prévue.
    """
    # Gère les noms de continents avec accents et caractères spéciaux
    if not continent:
        return "pirate"
    texte_nfd = unicodedata.normalize("NFKD", continent)  # Sépare les caractères des accents
    caracteres = []
    for caractere in texte_nfd:
        if not unicodedata.combining(caractere):  # Garde seulement les caractères de base
            caracteres.append(caractere)
    return "".join(caracteres).lower()


def _charger_chemins_niveau(numero_niveau):
    """
    A quoi sert la fonction : Charge les chemins spécifiques à un niveau depuis un fichier.
    Entrée : numero_niveau.
    Sortie : Retourne la valeur attendue ou applique l'action prévue.
    """
    # Construit le chemin vers le fichier de niveau
    base = os.path.dirname(__file__)
    chemin_fichier = os.path.join(base, "niveau_chemin", f"niveau{numero_niveau}.py")
    if not os.path.exists(chemin_fichier):
        return []  # Fichier non trouvé

    # Charge dynamiquement le module Python
    spec = importlib.util.spec_from_file_location(f"niveau_{numero_niveau}", chemin_fichier)
    if not spec or not spec.loader:
        return []  # Erreur de chargement
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception:
        return []  # Erreur d'exécution
    return getattr(module, "CHEMINS_VAGUES", [])  # Retourne les chemins de vagues


def _appliquer_variation_continent(chemin_de_base, continent):
    """
    A quoi sert la fonction : Applique des variations de position selon le continent.
    Entrée : chemin_de_base, continent.
    Sortie : Retourne la valeur attendue ou applique l'action prévue.
    """
    # Décalages selon le continent pour varier les chemins
    decalages = {
        "pirate": (0, 0),      # Référence
        "samourai": (0, -35),   # Plus haut
        "medieval": (0, 20),    # Plus bas
        "demoniaque": (0, 45),  # Encore plus bas
    }
    decalage_x, decalage_y = decalages.get(continent, (0, 0))
    
    # Applique les décalages en gardant les limites de l'écran
    chemin_modifie = []
    for x, y in chemin_de_base:
        nx = max(0, min(position_mur, x + decalage_x))  # Limite horizontal
        ny = max(80, min(hauteur_ecran - 20, y + decalage_y))  # Limite vertical
        chemin_modifie.append((nx, ny))
    
    # Force le dernier point sur le mur
    if chemin_modifie:
        chemin_modifie[-1] = (position_mur, chemin_modifie[-1][1])
    return chemin_modifie


def configurer_chemin_niveau_vague(continent, numero_niveau, numero_vague_dans_niveau):
    """
    A quoi sert la fonction : Configure le chemin selon le niveau et la vague spécifiques.
    Entrée : continent, numero_niveau, numero_vague_dans_niveau.
    Sortie : Retourne la valeur attendue ou applique l'action prévue.
    """
    # Normalise et charge les chemins du niveau
    continent = _normaliser_continent(continent)
    chemins_vagues = _charger_chemins_niveau(numero_niveau)
    
    # Si pas de chemins spécifiques, utilise le chemin par défaut du continent
    if not chemins_vagues:
        configurer_chemin_continent(continent)
        return
    
    # Choisit le chemin selon la vague (1-4)
    index = max(0, min(3, numero_vague_dans_niveau - 1))
    chemin_choisi = chemins_vagues[index]
    
    # Applique les variations du continent
    chemin_final = _appliquer_variation_continent(chemin_choisi, continent)
    CHEMIN[:] = chemin_final  # Met à jour le chemin global


def draw_decor(fenetre, pygame):
    """
    A quoi sert la fonction : Dessine les décors du niveau (inactif car on utilise des images de fond).
    Entrée : fenetre, pygame.
    Sortie : Retourne la valeur attendue ou applique l'action prévue.
    """
    pass  # Les décors viennent maintenant de l'image de fond du continent


def draw_path(fenetre, pygame):
    """
    A quoi sert la fonction : Dessine le mur à la fin du chemin.
    Entrée : fenetre, pygame.
    Sortie : Retourne la valeur attendue ou applique l'action prévue.
    """
    # Dessine le mur protecteur à la droite de l'écran
    rect_mur = pygame.Rect(position_mur, 0, largeur_ecran - position_mur, hauteur_ecran)
    fenetre.fill(couleur_wall, rect_mur)
