"""
A quoi sert le fichier : Ce fichier gère la préparation des données avant la sauvegarde en convertissant les objets complexes du jeu en dictionnaires simples compatibles JSON. Il extrait les informations importantes des objets de progression, ajoute la date et l'heure actuelles, et structure toutes les données dans un format standardisé qui peut être facilement sauvegardé et rechargé plus tard.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu.
"""

from datetime import datetime


def _copie_niveaux_conquis(progression_monde):
    """
    A quoi sert la fonction : Extrait et copie les niveaux conquis de l'objet de progression du monde dans un dictionnaire simple pour la sauvegarde.
    Entrée : progression_monde (l'objet contenant les niveaux conquis à copier).
    Sortie : Retourne un dictionnaire avec les niveaux conquis par continent, ou un dictionnaire vide si progression_monde est None.
    """
    resultat = {}
    if progression_monde is None:
        return resultat
    for continent, liste in progression_monde.niveaux_conquis.items():
        resultat[continent] = list(liste)
    return resultat


def _copie_succes_vagues(progression_monde):
    """
    A quoi sert la fonction : Extrait et copie les succès de vagues de l'objet de progression du monde dans un dictionnaire simple pour la sauvegarde.
    Entrée : progression_monde (l'objet contenant les succès de vagues à copier).
    Sortie : Retourne un dictionnaire avec les succès de vagues par continent et par niveau, ou un dictionnaire vide si progression_monde est None.
    """
    resultat = {}
    if progression_monde is None:
        return resultat
    for continent, liste_niveaux in progression_monde.succes_vagues.items():
        nouveau = []
        for ligne in liste_niveaux:
            nouveau.append(list(ligne))
        resultat[continent] = nouveau
    return resultat


def fabriquer_dict_sauvegarde(nom_final, progression_monde, progression_joueur=None):
    """
    A quoi sert la fonction : Crée le dictionnaire complet de sauvegarde en assemblant toutes les données nécessaires : nom, date, niveau du joueur, niveaux conquis et succès de vagues.
    Entrée : nom_final (le nom final de la sauvegarde), progression_monde (les données de progression du monde), progression_joueur (les données de progression du joueur, optionnel).
    Sortie : Retourne un dictionnaire structuré contenant toutes les informations à sauvegarder.
    """
    niveau_joueur = 1
    if progression_joueur is not None and hasattr(progression_joueur, "niveau"):
        niveau_joueur = int(progression_joueur.niveau)

    return {
        "nom": nom_final,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "niveau_joueur": niveau_joueur,
        "niveaux_conquis": _copie_niveaux_conquis(progression_monde),
        "succès_vagues": _copie_succes_vagues(progression_monde),
    }
