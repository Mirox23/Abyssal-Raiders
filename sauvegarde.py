"""
Qu'est-ce que le fichier gère :
    Tout le système de sauvegarde et chargement de parties.
    Les données sont stockées dans un fichier JSON dans le dossier 'sauvegardes/'.
Entrée :
    Nom de la sauvegarde, données de progression (niveaux conquis, argent, etc.)
Résultat :
    Fichiers JSON lisibles, liste des sauvegardes disponibles, chargement des données.
"""

import json
import os
from datetime import datetime

# Dossier où les sauvegardes sont stockées
DOSSIER_SAUVEGARDES = "sauvegardes"


def _assurer_dossier():
    """
    Explication : Crée le dossier de sauvegardes s'il n'existe pas encore.
    Les entrées : aucune
    Le résultat : dossier 'sauvegardes/' créé sur le disque si absent
    """
    if not os.path.exists(DOSSIER_SAUVEGARDES):
        os.makedirs(DOSSIER_SAUVEGARDES)


def sauvegarder(nom, progression_monde, progression_joueur=None):
    """
    Explication : Sauvegarde la progression complète dans un fichier JSON nommé par le joueur.
    Les entrées :
        nom (str) : le nom choisi par le joueur pour sa sauvegarde
        progression_monde (ProgressionMonde) : contient les niveaux conquis par continent
        progression_joueur (Progression ou None) : niveau XP du joueur, peut être None
    Le résultat : fichier JSON créé/écrasé dans le dossier sauvegardes/
    """
    _assurer_dossier()

    # On nettoie le nom pour éviter les caractères interdits dans les noms de fichiers
    nom_propre = "".join(c for c in nom if c.isalnum() or c in (" ", "_", "-")).strip()
    if not nom_propre:
        nom_propre = "partie_sans_nom"

    donnees = {
        "nom": nom_propre,
        "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "niveaux_conquis": progression_monde.niveaux_conquis,  # dict continent -> liste bool
        "succes_vagues": getattr(progression_monde, "succes_vagues", {}),
    }

    # Ajoute les infos du joueur si disponibles
    if progression_joueur is not None:
        donnees["niveau_joueur"] = progression_joueur.niveau
        donnees["xp_actuelle"] = progression_joueur.xp_actuelle

    chemin = os.path.join(DOSSIER_SAUVEGARDES, f"{nom_propre}.json")
    try:
        with open(chemin, "w", encoding="utf-8") as f:
            json.dump(donnees, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def charger(nom):
    """
    Explication : Charge une sauvegarde depuis son nom et retourne les données brutes.
    Les entrées :
        nom (str) : nom de la sauvegarde (sans l'extension .json)
    Le résultat :
        dict avec les données de la sauvegarde, ou None si le fichier n'existe pas
    """
    chemin = os.path.join(DOSSIER_SAUVEGARDES, f"{nom}.json")
    if not os.path.exists(chemin):
        return None
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def lister_sauvegardes():
    """
    Explication : Retourne la liste de toutes les sauvegardes disponibles avec leurs infos.
    Les entrées : aucune
    Le résultat :
        liste de dicts {"nom", "date", "niveau_joueur"} triée par date (plus récente d'abord)
    """
    _assurer_dossier()
    resultats = []
    for fichier in os.listdir(DOSSIER_SAUVEGARDES):
        if not fichier.endswith(".json"):
            continue
        chemin = os.path.join(DOSSIER_SAUVEGARDES, fichier)
        try:
            with open(chemin, "r", encoding="utf-8") as f:
                data = json.load(f)
            resultats.append({
                "nom": data.get("nom", fichier[:-5]),
                "date": data.get("date", "Inconnue"),
                "niveau_joueur": data.get("niveau_joueur", 1),
            })
        except Exception:
            pass
    # Tri : plus récente en premier (comparaison alphabétique de la date formatée)
    resultats.sort(key=lambda x: x["date"], reverse=True)
    return resultats


def supprimer(nom):
    """
    Explication : Supprime définitivement une sauvegarde du disque.
    Les entrées :
        nom (str) : nom de la sauvegarde à supprimer
    Le résultat : True si supprimé, False si le fichier n'existait pas
    """
    chemin = os.path.join(DOSSIER_SAUVEGARDES, f"{nom}.json")
    if os.path.exists(chemin):
        os.remove(chemin)
        return True
    return False


def appliquer_sauvegarde(donnees, progression_monde):
    """
    Explication : Injecte les données d'une sauvegarde dans l'objet ProgressionMonde.
    Les entrées :
        donnees (dict) : données brutes issues de charger()
        progression_monde (ProgressionMonde) : objet à remplir
    Le résultat : progression_monde modifié en place, retourne le niveau joueur (int)
    """
    if donnees is None:
        return 1

    # Recharge les niveaux conquis
    niveaux = donnees.get("niveaux_conquis", {})
    for continent, liste in niveaux.items():
        if continent in progression_monde.niveaux_conquis:
            # On s'assure que la longueur est correcte (8 niveaux)
            progression_monde.niveaux_conquis[continent] = (liste + [False] * 8)[:8]
    succes = donnees.get("succes_vagues", {})
    for continent, liste_niveaux in succes.items():
        if continent in progression_monde.succes_vagues:
            propre = []
            for ligne in liste_niveaux[:8]:
                ligne_ok = list(ligne) if isinstance(ligne, list) else [False, False, False]
                propre.append((ligne_ok + [False, False, False])[:3])
            while len(propre) < 8:
                propre.append([False, False, False])
            progression_monde.succes_vagues[continent] = propre

    return donnees.get("niveau_joueur", 1)
