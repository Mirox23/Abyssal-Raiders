"""
A quoi sert le fichier : Ce fichier génère automatiquement le contenu des vagues pour chaque niveau et continent. Il construit numériquement les quatre vagues qui composent un palier précis, en respectant les contraintes de nombre maximum d'ennemis, les types de mobs disponibles, et les temps d'apparition. Le module sait quels types d'ennemis utiliser pour chaque continent et fabrique des groupes variés avec des délais calibrés pour ne jamais dépasser les plafonds.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Retourne des dictionnaires structurés contenant les informations de spawn, les types d'ennemis, les intervalles et les groupes pour chaque vague.
"""

TYPES_PAR_CONTINENT = {
    "pirate": ["Mob", "MobRapide", "MobTank", "MobKamikaze", "MobSoigneur"],
    "samourai": ["MobRapide", "Mob", "MobTank", "MobSoigneur", "MobKamikaze"],
    "medieval": ["MobTank", "Mob", "MobRapide", "MobSoigneur", "MobKamikaze"],
    "demoniaque": ["MobKamikaze", "MobSoigneur", "MobTank", "MobRapide", "Mob"],
}


def _types_pour_continent(continent):
    """
    A quoi sert la fonction : Nettoie le nom du continent et retourne la liste des types de mobs disponibles pour ce continent.
    Entrée : continent (le nom du continent, possiblement avec accents, majuscules ou espaces).
    Sortie : Retourne la liste des classes de mobs utilisées pour le continent spécifié, ou les types pirates par défaut.
    """
    cle = str(continent).lower().strip()
    return TYPES_PAR_CONTINENT.get(cle, TYPES_PAR_CONTINENT["pirate"])


def _faire_groupe(type_mob, nombre, decalage, bonus_vitesse):
    """
    A quoi sert la fonction : Crée un dictionnaire structuré pour un groupe d'ennemis avec les paramètres validés.
    Entrée : type_mob (le type de mob), nombre (le nombre d'ennemis), decalage (le décalage en secondes), bonus_vitesse (le bonus de vitesse).
    Sortie : Retourne un dictionnaire formaté avec les contraintes appliquées.
    """
    return {
        "type": type_mob,
        "nombre": int(max(1, nombre)),
        "decalage": round(float(max(0.0, decalage)), 2),
        "bonus_vitesse": round(float(max(0.0, bonus_vitesse)), 2),
    }


def _generer_groupes(continent, niveau, numero_vague):
    """
    A quoi sert la fonction : Génère les groupes d'ennemis pour une vague spécifique en respectant la progression calibrée.
    Entrée : continent (le continent pour les types d'ennemis), niveau (le niveau de difficulté), numero_vague (le numéro de la vague).
    Sortie : Retourne une liste de groupes avec types, nombres, décalages et bonus de vitesse.
    """
    types = _types_pour_continent(continent)

    # Paramètres calibrés par niveau
    # base_v1  : nombre de mobs dans le 1er groupe à la vague 1
    # step     : mobs supplémentaires par vague (+step par vague suivante)
    # nb_g     : nombre de groupes (chaque groupe ajoute 1 mob de plus que le précédent)
    params = {
        1: {"base_v1": 4,  "step": 2, "nb_g": 2},
        2: {"base_v1": 6,  "step": 3, "nb_g": 3},
        3: {"base_v1": 9,  "step": 3, "nb_g": 4},
        4: {"base_v1": 11, "step": 3, "nb_g": 5},
        5: {"base_v1": 16, "step": 2, "nb_g": 5},
    }
    p = params.get(niveau, params[5])
    base  = p["base_v1"] + p["step"] * (numero_vague - 1)
    nb_g  = p["nb_g"]

    # Plafond dur : jamais plus de 100 mobs au total sur la vague
    PLAFOND_TOTAL = 100
    total_prevu = sum(base + i for i in range(nb_g))
    if total_prevu > PLAFOND_TOTAL:
        # Réduire la base pour respecter le plafond
        base = (PLAFOND_TOTAL - nb_g * (nb_g - 1) // 2) // nb_g

    groupes = []
    decalage = 0.0
    for index in range(nb_g):
        type_mob = types[(index + niveau + numero_vague) % len(types)]
        nombre = base + index
        bonus_vitesse = 0.01 * ((niveau + numero_vague + index) % 9)
        groupes.append(_faire_groupe(type_mob, nombre, decalage, bonus_vitesse))
        decalage += 0.5
    return groupes


def _generer_vague(continent, niveau, numero_vague):
    """
    A quoi sert la fonction : Détermine l'intervalle de spawn et agrège les groupes générés pour créer une vague complète.
    Entrée : continent (le nom du continent), niveau (le niveau de difficulté), numero_vague (le numéro de la vague entre 1 et 4).
    Sortie : Retourne un dictionnaire contenant l'intervalle, les groupes et un commentaire explicatif.
    """
    # Intervalle de spawn : plus espacé au niveau 1 pour laisser le temps de réagir
    intervalle = 1.1 - (niveau * 0.04) - (numero_vague * 0.04)
    intervalle = max(0.35, intervalle)
    return {
        "intervalle_spawn": round(intervalle, 2),
        "groupes": _generer_groupes(continent, niveau, numero_vague),
        "commentaire": "Progression calibree : ~9 mobs niveau 1 vague 1, ~100 mobs niveau 5.",
    }


def charger_configuration(continent, niveau):
    """
    A quoi sert la fonction : Génère les quatre vagues d'un niveau pour un continent donné en utilisant les paramètres calibrés.
    Entrée : continent (le nom du continent pour les types d'ennemis), niveau (le niveau de difficulté).
    Sortie : Retourne un dictionnaire avec les 4 vagues générées et leurs configurations.
    """
    niveau_int = int(max(1, niveau))
    return {
        1: _generer_vague(continent, niveau_int, 1),
        2: _generer_vague(continent, niveau_int, 2),
        3: _generer_vague(continent, niveau_int, 3),
        4: _generer_vague(continent, niveau_int, 4),
    }