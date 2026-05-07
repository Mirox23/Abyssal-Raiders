import json
import os

from sauvegarde_dossier_parties import DOSSIER_SAUVEGARDES, assurer_le_dossier
from sauvegarde_nom_joueur import rendre_nom_fichier_propre


def _chemin_depuis_nom(nom):
    nom_simple = rendre_nom_fichier_propre(nom)
    return os.path.join(DOSSIER_SAUVEGARDES, nom_simple + ".json")


def lire_dict_depuis_chemin(chemin):
    if not os.path.exists(chemin):
        return None
    try:
        with open(chemin, "r", encoding="utf-8") as fichier:
            return json.load(fichier)
    except Exception:
        return None


def ecrire_sauvegarde_json(nom, donnees):
    assurer_le_dossier()
    chemin = _chemin_depuis_nom(nom)
    try:
        with open(chemin, "w", encoding="utf-8") as fichier:
            json.dump(donnees, fichier, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def lire_sauvegarde_json(nom):
    chemin = _chemin_depuis_nom(nom)
    return lire_dict_depuis_chemin(chemin)
