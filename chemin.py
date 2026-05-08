from setting import (
    largeur_ecran, hauteur_ecran,
    position_mur, couleur_wall,
)
import importlib.util
import os
import unicodedata

CHEMINS_CONTINENTS = {
    "pirate": [
        (0, 210),
        (180, 210),
        (180, 355),
        (380, 355),
        (380, 130),
        (650, 130),
        (650, 410),
        (840, 410),
        (840, 275),
        (position_mur, 275),
    ],
    "samourai": [
        (0, 120),
        (160, 120),
        (160, 275),
        (330, 275),
        (330, 465),
        (570, 465),
        (570, 225),
        (760, 225),
        (760, 350),
        (position_mur, 350),
    ],
    "medieval": [
        (0, 300),
        (210, 300),
        (210, 180),
        (430, 180),
        (430, 350),
        (640, 350),
        (640, 160),
        (830, 160),
        (830, 300),
        (position_mur, 300),
    ],
    "demoniaque": [
        (0, 250),
        (140, 250),
        (140, 120),
        (320, 120),
        (320, 410),
        (500, 410),
        (500, 220),
        (700, 220),
        (700, 455),
        (position_mur, 455),
    ],
}

CHEMIN = list(CHEMINS_CONTINENTS["pirate"])

# Plus besoin des décors ronds rock/grass depuis qu'on a des images de fond par continent
liste_decors = []


def configurer_chemin_continent(continent):
    """
    Met à jour le chemin actif selon le continent choisi.
    On modifie la liste en place pour garder les références déjà importées.
    """
    cle_continent = _normaliser_continent(continent)
    chemin_continent = CHEMINS_CONTINENTS.get(cle_continent, CHEMINS_CONTINENTS["pirate"])
    CHEMIN[:] = chemin_continent


def _normaliser_continent(continent):
    if not continent:
        return "pirate"
    texte_nfd = unicodedata.normalize("NFKD", continent)  # Convertit les caractères accentués en caractères de base + accents séparés
    caracteres = []
    for caractere in texte_nfd:
        if not unicodedata.combining(caractere):
            caracteres.append(caractere)
    return "".join(caracteres).lower()


def _charger_chemins_niveau(numero_niveau):
    """
    Lit un fichier du dossier niveau chemin et retourne 4 chemins.
    Le fichier doit définir CHEMINS_VAGUES = [chemin1, chemin2, chemin3, chemin4].
    """
    base = os.path.dirname(__file__)
    chemin_fichier = os.path.join(base, "niveau_chemin", f"niveau{numero_niveau}.py")
    if not os.path.exists(chemin_fichier):
        return []

    spec = importlib.util.spec_from_file_location(f"niveau_{numero_niveau}", chemin_fichier)
    if not spec or not spec.loader:
        return []
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception:
        return []
    return getattr(module, "CHEMINS_VAGUES", [])


def _appliquer_variation_continent(chemin_de_base, continent):
    """
    Petite variation pour différencier visuellement les continents
    même avec la même structure de niveau.
    """
    decalages = {
        "pirate": (0, 0),
        "samourai": (0, -35),
        "medieval": (0, 20),
        "demoniaque": (0, 45),
    }
    decalage_x, decalage_y = decalages.get(continent, (0, 0))
    chemin_modifie = []
    for x, y in chemin_de_base:
        nx = max(0, min(position_mur, x + decalage_x))
        ny = max(80, min(hauteur_ecran - 20, y + decalage_y))
        chemin_modifie.append((nx, ny))
    if chemin_modifie:
        chemin_modifie[-1] = (position_mur, chemin_modifie[-1][1])
    return chemin_modifie


def configurer_chemin_niveau_vague(continent, numero_niveau, numero_vague_dans_niveau):
    """
    Configure le chemin actif pour une vague donnée.
    Chaque niveau contient 4 vagues avec 4 chemins dédiés.
    """
    continent = _normaliser_continent(continent)
    chemins_vagues = _charger_chemins_niveau(numero_niveau)
    if not chemins_vagues:
        configurer_chemin_continent(continent)
        return
    index = max(0, min(3, numero_vague_dans_niveau - 1))
    chemin_choisi = chemins_vagues[index]
    chemin_final = _appliquer_variation_continent(chemin_choisi, continent)
    CHEMIN[:] = chemin_final


def draw_decor(fenetre, pygame):
    pass  # Les décors viennent maintenant de l'image de fond du continent


def draw_path(fenetre, pygame):
    rect_mur = pygame.Rect(position_mur, 0, largeur_ecran - position_mur, hauteur_ecran)
    fenetre.fill(couleur_wall, rect_mur)
