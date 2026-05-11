"""
A quoi sert le fichier : Ce fichier gère la création et la vérification du dossier de sauvegardes du jeu. Il s'assure que le dossier 'sauvegardes' existe bien avant que le jeu essaie de sauvegarder ou charger des parties. C'est un module essentiel pour garantir que toutes les opérations de sauvegarde fonctionnent correctement en créant automatiquement le répertoire nécessaire s'il n'existe pas.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import os


DOSSIER_SAUVEGARDES = "sauvegardes"


def assurer_le_dossier():
    """
    A quoi sert la fonction : Vérifie si le dossier de sauvegardes existe et le crée automatiquement si nécessaire pour éviter les erreurs lors des opérations de sauvegarde.
    Entrée : Cette fonction ne demande pas de paramètre direct.
    Sortie : Crée le dossier 'sauvegardes' s'il n'existe pas déjà, ne fait rien s'il existe déjà.
    """
    if not os.path.exists(DOSSIER_SAUVEGARDES):
        os.makedirs(DOSSIER_SAUVEGARDES, exist_ok=True)



