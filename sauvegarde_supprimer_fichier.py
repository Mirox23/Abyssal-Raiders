"""
Qu'est-ce que le fichier gère : Ce fichier gère la partie sauvegarde supprimer fichier du projet.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Résultat : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import os

from sauvegarde_dossier_parties import DOSSIER_SAUVEGARDES
from sauvegarde_nom_joueur import rendre_nom_fichier_propre


def supprimer_fichier_de_sauvegarde(nom):
    """
    Explication de ce que fais la fonction : Cette fonction exécute supprimer fichier de sauvegarde.
    Les entrées : nom.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
    nom_simple = rendre_nom_fichier_propre(nom)
    chemin = os.path.join(DOSSIER_SAUVEGARDES, nom_simple + ".json")
    if not os.path.exists(chemin):
        return False
    try:
        os.remove(chemin)
        return True
    except Exception:
        return False
