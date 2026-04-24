"""
Système de scores locaux : sauvegarde les 5 meilleures runs par continent.
Format JSON : scores.json dans le dossier courant.
"""
import json
import os

FICHIER_SCORES = "scores.json"
MAX_SCORES_PAR_CONTINENT = 5


def _charger():
    if not os.path.exists(FICHIER_SCORES):
        return {}
    try:
        with open(FICHIER_SCORES, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _sauvegarder(data):
    try:
        with open(FICHIER_SCORES, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def enregistrer_score(continent, niveau, score, niveau_joueur):
    """Ajoute une entrée de score et ne garde que le top 5 par continent."""
    data = _charger()
    cle = continent
    if cle not in data:
        data[cle] = []
    entree = {
        "niveau": niveau,
        "score": score,
        "niveau_joueur": niveau_joueur,
    }
    data[cle].append(entree)
    # Tri décroissant par score et on coupe à MAX_SCORES_PAR_CONTINENT
    data[cle] = sorted(data[cle], key=lambda e: e["score"], reverse=True)[:MAX_SCORES_PAR_CONTINENT]
    _sauvegarder(data)


def obtenir_scores(continent):
    """Retourne la liste des meilleures entrées pour un continent."""
    data = _charger()
    return data.get(continent, [])


def obtenir_meilleur_score(continent):
    """Retourne le meilleur score pour un continent, ou 0."""
    scores = obtenir_scores(continent)
    if not scores:
        return 0
    return scores[0]["score"]