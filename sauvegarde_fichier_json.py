"""
Qu'est-ce que le fichier gère : Ce fichier gère la partie sauvegarde fichier json du projet.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Résultat : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import json
import os

from sauvegarde_dossier_parties import DOSSIER_SAUVEGARDES, assurer_le_dossier
from sauvegarde_nom_joueur import rendre_nom_fichier_propre


def _chemin_depuis_nom(nom):
    """
    Explication de ce que fais la fonction : Cette fonction exécute chemin depuis nom.
    Les entrées : nom.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
    nom_simple = rendre_nom_fichier_propre(nom)
    return os.path.join(DOSSIER_SAUVEGARDES, nom_simple + ".json")


def lire_dict_depuis_chemin(chemin):
    """
    Explication de ce que fais la fonction : Cette fonction exécute lire dict depuis chemin.
    Les entrées : chemin.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
    if not os.path.exists(chemin):
        return None
    try:
        with open(chemin, "r", encoding="utf-8") as fichier:
            return json.load(fichier)
    except Exception:
        return None


def ecrire_sauvegarde_json(nom, donnees):
    """
    Explication de ce que fais la fonction : Cette fonction exécute ecrire sauvegarde json.
    Les entrées : nom, donnees.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
    assurer_le_dossier()
    chemin = _chemin_depuis_nom(nom)
    try:
        with open(chemin, "w", encoding="utf-8") as fichier:
            json.dump(donnees, fichier, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def lire_sauvegarde_json(nom):
    """
    Explication de ce que fais la fonction : Cette fonction exécute lire sauvegarde json.
    Les entrées : nom.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
    chemin = _chemin_depuis_nom(nom)
    return lire_dict_depuis_chemin(chemin)
