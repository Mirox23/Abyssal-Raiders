"""
Qu'est-ce que le fichier gère : Ce fichier gère la partie sauvegarde lister fichiers du projet.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Résultat : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import os

import sauvegarde_fichier_json as sfj
from sauvegarde_dossier_parties import DOSSIER_SAUVEGARDES, assurer_le_dossier


def obtenir_liste_des_sauvegardes():
    """
    Explication de ce que fais la fonction : Cette fonction récupère obtenir liste des sauvegardes.
    Les entrées : Cette fonction ne demande pas de paramètre direct.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
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
