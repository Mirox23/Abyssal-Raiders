"""
A quoi sert le fichier : Ce fichier gère tout le système de sauvegarde du jeu. Il permet de sauvegarder et charger les parties des joueurs, de gérer les noms de fichiers, de créer les dossiers de sauvegarde, de préparer les données à sauvegarder, et d'appliquer les sauvegardes chargées. Il contient aussi des fonctions pour lister et supprimer les sauvegardes existantes.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu.
"""

# Importe tous les modules nécessaires pour la gestion des sauvegardes
from sauvegarde_dossier_parties import assurer_le_dossier
from sauvegarde_fichier_json import ecrire_sauvegarde_json, lire_sauvegarde_json
from sauvegarde_injecter_progression import copier_donnees_dans_progression
from sauvegarde_lister_fichiers import obtenir_liste_des_sauvegardes
from sauvegarde_nom_joueur import choisir_nom_final, rendre_nom_fichier_propre
from sauvegarde_preparation_donnees import fabriquer_dict_sauvegarde
from sauvegarde_supprimer_fichier import supprimer_fichier_de_sauvegarde


def _assurer_dossier():
    """
    A quoi sert la fonction : Assure que le dossier de sauvegarde existe.
    Entrée : Cette fonction ne demande pas de paramètre direct.
    Sortie : Retourne la valeur attendue ou applique l'action prévue.
    """
    # Crée le dossier de sauvegarde s'il n'existe pas
    assurer_le_dossier()


def sauvegarder(nom, progression_monde, progression_joueur=None):
    """
    A quoi sert la fonction : Sauvegarde une partie avec le nom donné.
    Entrée : nom, progression_monde, progression_joueur.
    Sortie : Retourne la valeur attendue ou applique l'action prévue.
    """
    # Prépare et écrit la sauvegarde
    _assurer_dossier()
    nom_nettoye = rendre_nom_fichier_propre(nom)  # Nettoie le nom pour le fichier
    nom_final = choisir_nom_final(nom_nettoye)  # Choisit le nom final unique
    donnees = fabriquer_dict_sauvegarde(nom_final, progression_monde, progression_joueur)  # Prépare les données
    ok = ecrire_sauvegarde_json(nom_final, donnees)  # Écrit dans le fichier JSON
    return ok


def charger(nom):
    """
    A quoi sert la fonction : Charge une sauvegarde depuis son nom.
    Entrée : nom.
    Sortie : Retourne la valeur attendue ou applique l'action prévue.
    """
    # Lit et retourne les données de la sauvegarde
    return lire_sauvegarde_json(nom)


def lister_sauvegardes():
    """
    A quoi sert la fonction : Liste toutes les sauvegardes existantes.
    Entrée : Cette fonction ne demande pas de paramètre direct.
    Sortie : Retourne la valeur attendue ou applique l'action prévue.
    """
    # Retourne la liste des sauvegardes disponibles
    return obtenir_liste_des_sauvegardes()


def supprimer(nom):
    """
    A quoi sert la fonction : Supprime une sauvegarde spécifique.
    Entrée : nom.
    Sortie : Retourne la valeur attendue ou applique l'action prévue.
    """
    # Supprime le fichier de sauvegarde
    return supprimer_fichier_de_sauvegarde(nom)


def appliquer_sauvegarde(donnees, progression_monde):
    """
    A quoi sert la fonction : Applique les données d'une sauvegarde à la progression.
    Entrée : donnees, progression_monde.
    Sortie : Retourne la valeur attendue ou applique l'action prévue.
    """
    # Copie les données de la sauvegarde dans la progression actuelle
    return copier_donnees_dans_progression(donnees, progression_monde)
