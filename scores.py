"""
Qu'est-ce que le fichier gère : Ce fichier gère la partie scores du projet.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Résultat : Des comportements, calculs ou affichages utilisés par le jeu.
"""
import json
import os

FICHIER_SCORES = "scores.json"
MAX_SCORES_PAR_CONTINENT = 5


def _charger():
    """
    Explication de ce que fais la fonction : Cette fonction exécute charger.
    Les entrées : Cette fonction ne demande pas de paramètre direct.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
    if not os.path.exists(FICHIER_SCORES):
        return {}
    try:
        with open(FICHIER_SCORES, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _sauvegarder(data):
    """
    Explication de ce que fais la fonction : Cette fonction exécute sauvegarder.
    Les entrées : data.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
    try:
        with open(FICHIER_SCORES, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def _normaliser_data_continent(data_continent):
    """
    Explication de ce que fais la fonction : Cette fonction exécute normaliser data continent.
    Les entrées : data_continent.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
    if isinstance(data_continent, list):
        return {"top_runs": data_continent, "meilleurs_par_vague": {}}
    if isinstance(data_continent, dict):
        if "top_runs" not in data_continent:
            data_continent["top_runs"] = []
        if "meilleurs_par_vague" not in data_continent:
            data_continent["meilleurs_par_vague"] = {}
        return data_continent
    return {"top_runs": [], "meilleurs_par_vague": {}}


def enregistrer_score(continent, niveau, score, niveau_joueur, numero_vague=None, temps_vague=None, nom_joueur="Joueur"):
    """
    Explication de ce que fais la fonction : Cette fonction exécute enregistrer score.
    Les entrées : continent, niveau, score, niveau_joueur, numero_vague, temps_vague, nom_joueur.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
    data = _charger()
    cle = continent
    if cle not in data:
        data[cle] = {"top_runs": [], "meilleurs_par_vague": {}}
    data[cle] = _normaliser_data_continent(data[cle])
    entree = {
        "niveau": niveau,
        "score": score,
        "niveau_joueur": niveau_joueur,
        "nom_joueur": nom_joueur,
    }
    data[cle]["top_runs"].append(entree)
    # Tri décroissant par score et on coupe à MAX_SCORES_PAR_CONTINENT
    data[cle]["top_runs"] = sorted(data[cle]["top_runs"], key=lambda e: e["score"], reverse=True)[:MAX_SCORES_PAR_CONTINENT]

    if numero_vague is not None and temps_vague is not None:
        cle_vague = str(numero_vague)
        meilleur_actuel = data[cle]["meilleurs_par_vague"].get(cle_vague)
        if meilleur_actuel is None or temps_vague < meilleur_actuel.get("temps", 999999):
            data[cle]["meilleurs_par_vague"][cle_vague] = {
                "nom_joueur": nom_joueur,
                "temps": round(float(temps_vague), 2),
                "score": int(score),
            }

    _sauvegarder(data)


def obtenir_scores(continent):
    """
    Explication de ce que fais la fonction : Cette fonction récupère obtenir scores.
    Les entrées : continent.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
    data = _charger()
    data_continent = _normaliser_data_continent(data.get(continent, []))
    return data_continent["top_runs"]


def obtenir_meilleurs_par_vague(continent):
    """
    Explication de ce que fais la fonction : Cette fonction récupère obtenir meilleurs par vague.
    Les entrées : continent.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
    data = _charger()
    data_continent = _normaliser_data_continent(data.get(continent, []))
    return data_continent["meilleurs_par_vague"]


def obtenir_meilleur_score(continent):
    """
    Explication de ce que fais la fonction : Cette fonction récupère obtenir meilleur score.
    Les entrées : continent.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
    scores = obtenir_scores(continent)
    if not scores:
        return 0
    return scores[0]["score"]
