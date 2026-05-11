"""
A quoi sert le fichier : Ce fichier gère tout le système de sauvegarde du jeu. Il permet de sauvegarder la progression du joueur, les niveaux débloqués, l'argent, l'expérience et toutes les données importantes. Il contient les fonctions pour créer des fichiers de sauvegarde, les charger, les lister et les supprimer. Il gère aussi la validation des noms de fichiers et l'organisation du dossier de sauvegardes.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu.
"""

from sauvegarde_dossier_parties import assurer_le_dossier
from sauvegarde_fichier_json import ecrire_sauvegarde_json, lire_sauvegarde_json
from sauvegarde_injecter_progression import copier_donnees_dans_progression
from sauvegarde_lister_fichiers import obtenir_liste_des_sauvegardes
from sauvegarde_nom_joueur import choisir_nom_final, rendre_nom_fichier_propre
from sauvegarde_preparation_donnees import fabriquer_dict_sauvegarde
from sauvegarde_supprimer_fichier import supprimer_fichier_de_sauvegarde


def _assurer_dossier():
    """
    Explication de ce que fais la fonction : Cette fonction exécute assurer dossier.
    Les entrées : Cette fonction ne demande pas de paramètre direct.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
    assurer_le_dossier()


def sauvegarder(nom, progression_monde, progression_joueur=None):
    """
    Explication de ce que fais la fonction : Cette fonction exécute sauvegarder.
    Les entrées : nom, progression_monde, progression_joueur.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
    _assurer_dossier()
    nom_nettoye = rendre_nom_fichier_propre(nom)
    nom_final = choisir_nom_final(nom_nettoye)
    donnees = fabriquer_dict_sauvegarde(nom_final, progression_monde, progression_joueur)
    ok = ecrire_sauvegarde_json(nom_final, donnees)
    return ok


def charger(nom):
    """
    Explication de ce que fais la fonction : Cette fonction exécute charger.
    Les entrées : nom.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
    return lire_sauvegarde_json(nom)


def lister_sauvegardes():
    """
    Explication de ce que fais la fonction : Cette fonction exécute lister sauvegardes.
    Les entrées : Cette fonction ne demande pas de paramètre direct.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
    return obtenir_liste_des_sauvegardes()


def supprimer(nom):
    """
    Explication de ce que fais la fonction : Cette fonction exécute supprimer.
    Les entrées : nom.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
    return supprimer_fichier_de_sauvegarde(nom)


def appliquer_sauvegarde(donnees, progression_monde):
    """
    Explication de ce que fais la fonction : Cette fonction exécute appliquer sauvegarde.
    Les entrées : donnees, progression_monde.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
    return copier_donnees_dans_progression(donnees, progression_monde)
