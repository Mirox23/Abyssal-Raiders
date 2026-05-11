"""
A quoi sert le fichier : Ce fichier gère le traitement et la validation des noms de fichiers de sauvegarde. Il nettoie les noms des joueurs pour les rendre compatibles avec les systèmes de fichiers, supprime les caractères spéciaux, et évite les conflits de noms en ajoutant des indices si nécessaire. C'est essentiel pour garantir que chaque sauvegarde ait un nom de fichier unique et valide.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import os
import re

from sauvegarde_dossier_parties import DOSSIER_SAUVEGARDES, assurer_le_dossier


def rendre_nom_fichier_propre(nom):
    """
    A quoi sert la fonction : Nettoie le nom du joueur en le convertissant en minuscules, en remplaçant les espaces par des underscores et en supprimant tous les caractères spéciaux pour créer un nom de fichier valide.
    Entrée : nom (le nom du joueur à nettoyer).
    Sortie : Retourne une chaîne de caractères nettoyée et compatible avec les systèmes de fichiers.
    """
    texte = str(nom).strip().lower()
    if not texte:
        return "partie"
    texte = texte.replace(" ", "_")
    texte = re.sub(r"[^a-z0-9_-]", "", texte)
    if not texte:
        return "partie"
    return texte


def choisir_nom_final(nom_sans_extension):
    """
    A quoi sert la fonction : Génère un nom de fichier unique en évitant les conflits avec des sauvegardes existantes en ajoutant des indices numériques si nécessaire.
    Entrée : nom_sans_extension (le nom de base souhaité pour la sauvegarde).
    Sortie : Retourne un nom de fichier unique qui n'existe pas encore dans le dossier de sauvegardes.
    """
    assurer_le_dossier()
    base = nom_sans_extension
    candidat = base
    index = 1
    while True:
        chemin = os.path.join(DOSSIER_SAUVEGARDES, candidat + ".json")
        if not os.path.exists(chemin):
            return candidat
        candidat = f"{base}_{index}"
        index += 1
