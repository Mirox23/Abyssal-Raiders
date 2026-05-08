"""
Point d'entrée du système de sauvegarde : les grosses fonctions sont dans d'autres fichiers.
"""

from sauvegarde_dossier_parties import assurer_le_dossier
from sauvegarde_fichier_json import ecrire_sauvegarde_json, lire_sauvegarde_json
from sauvegarde_injecter_progression import copier_donnees_dans_progression
from sauvergarde_lister_fichiers import obtenir_liste_des_sauvegardes
from sauvegarde_nom_joueur import choisir_nom_final, rendre_nom_fichier_propre
from sauvegarde_preparation_donnees import fabriquer_dict_sauvegarde
from sauvegarde_supprimer_fichier import supprimer_fichier_de_sauvegarde


def _assurer_dossier():
    assurer_le_dossier()


def sauvegarder(nom, progression_monde, progression_joueur=None):
    _assurer_dossier()
    nom_nettoye = rendre_nom_fichier_propre(nom)
    nom_final = choisir_nom_final(nom_nettoye)
    donnees = fabriquer_dict_sauvegarde(nom_final, progression_monde, progression_joueur)
    ok = ecrire_sauvegarde_json(nom_final, donnees)
    return ok


def charger(nom):
    return lire_sauvegarde_json(nom)


def lister_sauvegardes():
    return obtenir_liste_des_sauvegardes()


def supprimer(nom):
    return supprimer_fichier_de_sauvegarde(nom)


def appliquer_sauvegarde(donnees, progression_monde):
    return copier_donnees_dans_progression(donnees, progression_monde)
