"""
A quoi sert le fichier : Ce fichier gère le système de scores et de classements du jeu. Il permet d'enregistrer les scores des joueurs dans un fichier JSON, de maintenir les meilleurs scores par continent et par vague, et d'afficher les classements. Il contient les fonctions pour charger, sauvegarder et trier les scores, ainsi que pour ajouter de nouvelles performances au classement.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu.
"""
import json
import os

fichier_scores = "scores.json"
max_scores_par_continent = 5
# Nombre maximum de joueurs conservés dans le classement par vague
max_joueurs_par_vague = 4


def _charger():
    """
    Explication de ce que fais la fonction : Cette fonction exécute charger.
    Les entrées : Cette fonction ne demande pas de paramètre direct.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
    if not os.path.exists(fichier_scores):
        return {}
    try:
        with open(fichier_scores, "r", encoding="utf-8") as f:
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
        with open(fichier_scores, "w", encoding="utf-8") as f:
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
        return {"top_runs": data_continent, "classement_par_vague": {}}
    if isinstance(data_continent, dict):  # isinstance vérifie si data_continent est un dictionnaire
        if "top_runs" not in data_continent:
            data_continent["top_runs"] = []
        # Migration : ancienne clé meilleurs_par_vague → classement_par_vague
        if "meilleurs_par_vague" in data_continent and "classement_par_vague" not in data_continent:
            ancienne = data_continent.pop("meilleurs_par_vague")
            # Convertir l'ancien format (un seul record) vers le nouveau (liste)
            nouveau = {}
            for cle_vague, entree in ancienne.items():
                if isinstance(entree, dict):
                    nouveau[cle_vague] = [entree]
                else:
                    nouveau[cle_vague] = []
            data_continent["classement_par_vague"] = nouveau
        if "classement_par_vague" not in data_continent:
            data_continent["classement_par_vague"] = {}
        return data_continent
    return {"top_runs": [], "classement_par_vague": {}}


def enregistrer_score(continent, niveau, score, niveau_joueur, numero_vague=None, temps_vague=None, nom_joueur="Joueur"):
    """
    Explication de ce que fais la fonction : Cette fonction exécute enregistrer score.
    Les entrées : continent, niveau, score, niveau_joueur, numero_vague, temps_vague, nom_joueur.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
    data = _charger()
    cle = continent
    if cle not in data:
        data[cle] = {"top_runs": [], "classement_par_vague": {}}
    data[cle] = _normaliser_data_continent(data[cle])

    entree = {
        "niveau": niveau,
        "score": score,
        "niveau_joueur": niveau_joueur,
        "nom_joueur": nom_joueur,
    }
    data[cle]["top_runs"].append(entree)
    # Tri décroissant par score et on coupe à max_scores_par_continent
    data[cle]["top_runs"] = sorted(
        data[cle]["top_runs"], key=lambda e: e["score"], reverse=True
    )[:max_scores_par_continent]

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
    Explication de ce que fais la fonction : Cette fonction récupère obtenir scores.
    Les entrées : continent.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
    data = _charger()
    data_continent = _normaliser_data_continent(data.get(continent, []))
    return data_continent["top_runs"]


def obtenir_classement_par_vague(continent):
    """
    Explication de ce que fais la fonction : Cette fonction récupère le classement des meilleurs temps par vague.
    Les entrées : continent.
    Le résultat : Retourne un dict {numero_vague: [liste triée d'entrées]} avec au plus max_joueurs_par_vague entrées.
    """
    data = _charger()
    data_continent = _normaliser_data_continent(data.get(continent, {}))
    return data_continent.get("classement_par_vague", {})


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