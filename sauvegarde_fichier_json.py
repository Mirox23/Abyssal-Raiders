"""
A quoi sert le fichier : Ce fichier gère toutes les opérations de lecture et d'écriture des fichiers de sauvegarde au format JSON. Il contient les fonctions pour convertir les données de jeu en format JSON, écrire les sauvegardes dans des fichiers, lire les sauvegardes existantes, et gérer les chemins des fichiers. C'est le module technique qui permet de transformer les objets Python en données persistantes stockées sur le disque dur.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import json
import os

from sauvegarde_dossier_parties import DOSSIER_SAUVEGARDES, assurer_le_dossier
from sauvegarde_nom_joueur import rendre_nom_fichier_propre


def _chemin_depuis_nom(nom):
    """
    A quoi sert la fonction : Construit le chemin complet du fichier de sauvegarde à partir du nom du joueur en nettoyant le nom et en ajoutant l'extension .json.
    Entrée : nom (le nom du joueur pour la sauvegarde).
    Sortie : Retourne le chemin complet du fichier sous forme de chaîne de caractères.
    """
    nom_simple = rendre_nom_fichier_propre(nom)
    return os.path.join(DOSSIER_SAUVEGARDES, nom_simple + ".json")


def lire_dict_depuis_chemin(chemin):
    """
    A quoi sert la fonction : Lit un fichier JSON et le convertit en dictionnaire Python, en gérant les erreurs si le fichier n'existe pas ou est corrompu.
    Entrée : chemin (le chemin complet du fichier JSON à lire).
    Sortie : Retourne le dictionnaire contenu dans le fichier, ou un dictionnaire vide en cas d'erreur.
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
    A quoi sert la fonction : Sauvegarde les données de jeu dans un fichier JSON en s'assurant que le dossier existe et en gérant les erreurs d'écriture.
    Entrée : nom (le nom du joueur pour le fichier de sauvegarde), donnees (le dictionnaire contenant toutes les données à sauvegarder).
    Sortie : Retourne True si la sauvegarde a réussi, False en cas d'erreur.
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
    A quoi sert la fonction : Lit le fichier de sauvegarde d'un joueur et le convertit en dictionnaire Python pour restaurer sa partie.
    Entrée : nom (le nom du joueur dont on veut charger la sauvegarde).
    Sortie : Retourne le dictionnaire contenant les données de sauvegarde, ou None si le fichier n'existe pas ou est corrompu.
    """
    chemin = _chemin_depuis_nom(nom)
    return lire_dict_depuis_chemin(chemin)
