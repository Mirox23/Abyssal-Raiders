"""
A quoi sert le fichier : Ce fichier gère la liste des sauvegardes disponibles pour le joueur. Il scanne le dossier de sauvegardes, lit tous les fichiers JSON valides, et extrait les informations importantes comme le nom du joueur, la date de sauvegarde et le niveau atteint. Il présente ces données de manière organisée pour que le menu puisse afficher la liste des parties à charger.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import os

import sauvegarde_fichier_json as sfj
from sauvegarde_dossier_parties import DOSSIER_SAUVEGARDES, assurer_le_dossier


def obtenir_liste_des_sauvegardes():
    """
    A quoi sert la fonction : Scan le dossier de sauvegardes, lit tous les fichiers JSON valides et retourne une liste organisée des informations de chaque sauvegarde.
    Entrée : Cette fonction ne demande pas de paramètre direct.
    Sortie : Retourne une liste de dictionnaires contenant le nom, la date et le niveau de chaque sauvegarde, triée par date décroissante.
    """
    assurer_le_dossier()
    resultats = []
    fichiers = os.listdir(DOSSIER_SAUVEGARDES)
    for nom_fichier in fichiers:
        finit_par_json = nom_fichier.endswith(".json")
        if finit_par_json is False:
            continue
        chemin = os.path.join(DOSSIER_SAUVEGARDES, nom_fichier)
        data = sfj.lire_dict_depuis_chemin(chemin)
        if data is None:
            continue
        info = {
            "nom": data.get("nom", nom_fichier[:-5]),
            "date": data.get("date", "Inconnue"),
            "niveau_joueur": data.get("niveau_joueur", 1),
        }
        resultats.append(info)
    resultats.sort(key=lambda x: x["date"], reverse=True)
    return resultats
