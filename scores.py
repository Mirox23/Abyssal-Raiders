"""
A quoi sert le fichier : Ce fichier gère le système de scores et de classement du jeu. Il contient les fonctions pour charger, sauvegarder et normaliser les scores des joueurs, ainsi que pour limiter le nombre de scores conservés par continent et par vague. Il permet aussi de trier les scores et de gérer le classement des meilleurs joueurs.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu.
"""
# Importe les bibliothèques nécessaires pour la gestion des scores
import json
import os

# Fichier et constantes pour la gestion des scores
fichier_scores = "scores.json"  # Fichier de sauvegarde des scores
max_scores_par_continent = 5  # Nombre maximum de scores conservés par continent
max_joueurs_par_vague = 4  # Nombre maximum de joueurs conservés par vague


def _charger():
    """
    A quoi sert la fonction : Charge les scores depuis le fichier JSON.
    Entrée : Cette fonction ne demande pas de paramètre direct.
    Sortie : Retourne la valeur attendue ou applique l'action prévue.
    """
    # Vérifie si le fichier de scores existe
    if not os.path.exists(fichier_scores):
        return {}  # Retourne un dictionnaire vide si le fichier n'existe pas
    
    try:
        # Ouvre et charge le fichier JSON avec encodage UTF-8
        with open(fichier_scores, "r", encoding="utf-8") as f:
            return json.load(f)  # Charge et retourne les données JSON
    except Exception:
        return {}  # Retourne un dictionnaire vide en cas d'erreur


def _sauvegarder(data):
    """
    A quoi sert la fonction : Sauvegarde les scores dans le fichier JSON.
    Entrée : data.
    Sortie : Retourne la valeur attendue ou applique l'action prévue.
    """
    try:
        # Ouvre le fichier en écriture avec encodage UTF-8 et sauvegarde les données
        with open(fichier_scores, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)  # Sauvegarde avec indentation
    except Exception:
        pass  # Ignore les erreurs de sauvegarde


def _normaliser_data_continent(data_continent):
    """
    A quoi sert la fonction : Normalise et structure les données de scores par continent.
    Entrée : data_continent.
    Sortie : Retourne la valeur attendue ou applique l'action prévue.
    """
    if isinstance(data_continent, list):
        return {"top_runs": data_continent, "classement_par_vague": {}}
    
    if isinstance(data_continent, dict):
        # Normalise classement_par_vague si les entrées sont des dicts et non des listes
        if "classement_par_vague" in data_continent:
            ancienne = data_continent["classement_par_vague"]
            nouveau = {}
            for cle_vague, entree in ancienne.items():
                if isinstance(entree, dict):
                    nouveau[cle_vague] = [entree]
                elif isinstance(entree, list):
                    nouveau[cle_vague] = entree
                else:
                    nouveau[cle_vague] = []
            data_continent["classement_par_vague"] = nouveau
        else:
            data_continent["classement_par_vague"] = {}

        if "top_runs" not in data_continent:
            data_continent["top_runs"] = []

        return data_continent

    return {"top_runs": [], "classement_par_vague": {}}


def enregistrer_score(continent, niveau, score, niveau_joueur, numero_vague=None, temps_vague=None, nom_joueur="Joueur"):
    """
    A quoi sert la fonction : Enregistre un nouveau score dans le classement.
    Entrée : continent, niveau, score, niveau_joueur, numero_vague, temps_vague, nom_joueur.
    Sortie : Retourne la valeur attendue ou applique l'action prévue.
    """
    # Charge les scores existants
    data = _charger()
    cle = continent  # Clé du continent
    
    # Crée le continent s'il n'existe pas
    if cle not in data:
        data[cle] = {"top_runs": [], "classement_par_vague": {}}  # Structure par défaut
    data[cle] = _normaliser_data_continent(data[cle])  # Normalise les données
    
    # Prépare l'entrée pour le nouveau score
    entree = {
        "niveau": niveau,
        "score": score,
        "niveau_joueur": niveau_joueur,
        "nom_joueur": nom_joueur,
    }
    data[cle]["top_runs"].append(entree)  # Ajoute l'entrée au classement
    
    # Tri décroissant par score et limite au maximum
    data[cle]["top_runs"] = sorted(
        data[cle]["top_runs"], key=lambda e: e["score"], reverse=True
    )[:max_scores_par_continent]  # Garde seulement les meilleurs scores

    # Enregistrement du classement par vague : liste des max_joueurs_par_vague meilleurs temps
    if numero_vague is not None and temps_vague is not None:
        cle_vague = str(numero_vague)
        classement = data[cle]["classement_par_vague"].get(cle_vague, [])
        if not isinstance(classement, list):
            classement = []

        # Ajouter la nouvelle entrée
        nouvelle_entree = {
            "nom_joueur": nom_joueur,
            "temps": round(float(temps_vague), 2),
            "score": int(score),
        }
        classement.append(nouvelle_entree)

        # Trier par temps croissant (le plus rapide en premier) et garder les meilleurs
        classement = sorted(classement, key=lambda e: e["temps"])[:max_joueurs_par_vague]
        data[cle]["classement_par_vague"][cle_vague] = classement

    _sauvegarder(data)


def obtenir_scores(continent):
    """
    A quoi sert la fonction : Récupère la liste des scores pour un continent.
    Entrée : continent.
    Sortie : Retourne la valeur attendue ou applique l'action prévue.
    """
    # Charge les données et normalise la structure du continent
    data = _charger()
    data_continent = _normaliser_data_continent(data.get(continent, []))
    
    return data_continent["top_runs"]  # Retourne la liste des scores


def obtenir_classement_par_vague(continent):
    """
    A quoi sert la fonction : Récupère le classement des meilleurs temps par vague.
    Entrée : continent.
    Sortie : Retourne un dict {numero_vague: [liste triée d'entrées]} avec au plus max_joueurs_par_vague entrées.
    """
    # Charge et normalise les données du continent
    data = _charger()
    data_continent = _normaliser_data_continent(data.get(continent, {}))
    
    return data_continent.get("classement_par_vague", {})


def obtenir_meilleur_score(continent):
    """
    A quoi sert la fonction : Récupère le meilleur score pour un continent.
    Entrée : continent.
    Sortie : Retourne la valeur attendue ou applique l'action prévue.
    """
    # Récupère tous les scores du continent
    scores = obtenir_scores(continent)
    
    # Retourne le meilleur score ou 0 s'il n'y a pas de scores
    if not scores:
        return 0
    
    return scores[0]["score"]  # Le premier score est le meilleur (trié décroissant)