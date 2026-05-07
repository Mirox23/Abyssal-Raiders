import os

from sauvegarde_dossier_parties import DOSSIER_SAUVEGARDES
from sauvegarde_nom_joueur import rendre_nom_fichier_propre


def supprimer_fichier_de_sauvegarde(nom):
    nom_simple = rendre_nom_fichier_propre(nom)
    chemin = os.path.join(DOSSIER_SAUVEGARDES, nom_simple + ".json")
    if not os.path.exists(chemin):
        return False
    try:
        os.remove(chemin)
        return True
    except Exception:
        return False
