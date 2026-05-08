"""
Qu'est-ce que le fichier gère : Ce fichier gère la partie sauvegarde nom joueur du projet.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Résultat : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import os
import re

from sauvegarde_dossier_parties import DOSSIER_SAUVEGARDES, assurer_le_dossier


def rendre_nom_fichier_propre(nom):
    """
    Explication de ce que fais la fonction : Cette fonction exécute rendre nom fichier propre.
    Les entrées : nom.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
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
    Explication de ce que fais la fonction : Cette fonction exécute choisir nom final.
    Les entrées : nom_sans_extension.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
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
