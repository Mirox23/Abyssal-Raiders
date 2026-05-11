"""
A quoi sert le fichier : Ce fichier gère la suppression des fichiers de sauvegarde du jeu. Il permet de supprimer définitivement une sauvegarde en utilisant le nom du joueur, en nettoyant d'abord le nom pour le rendre compatible avec le système de fichiers, puis en supprimant le fichier JSON correspondant. C'est utile pour gérer l'espace de stockage et permettre aux joueurs de supprimer d'anciennes parties.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import os

from sauvegarde_dossier_parties import DOSSIER_SAUVEGARDES
from sauvegarde_nom_joueur import rendre_nom_fichier_propre


def supprimer_fichier_de_sauvegarde(nom):
    """
    A quoi sert la fonction : Supprime le fichier de sauvegarde correspondant au nom du joueur après avoir nettoyé le nom pour le rendre compatible avec les fichiers.
    Entrée : nom (le nom du joueur dont on veut supprimer la sauvegarde).
    Sortie : Retourne True si la suppression a réussi, False si le fichier n'existe pas ou en cas d'erreur.
    """
    nom_simple = rendre_nom_fichier_propre(nom)
    chemin = os.path.join(DOSSIER_SAUVEGARDES, nom_simple + ".json")
    if not os.path.exists(chemin):
        return True  # Le fichier n'existe pas, donc "suppression réussie"
    try:
        os.remove(chemin)
        return True
    except Exception:
        return False
