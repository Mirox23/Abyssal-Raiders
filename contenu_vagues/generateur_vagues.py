TYPES_PAR_CONTINENT = {
    "pirate": ["Mob", "MobRapide", "MobTank", "MobKamikaze", "MobSoigneur"],
    "samourai": ["MobRapide", "Mob", "MobTank", "MobSoigneur", "MobKamikaze"],
    "medieval": ["MobTank", "Mob", "MobRapide", "MobSoigneur", "MobKamikaze"],
    "demoniaque": ["MobKamikaze", "MobSoigneur", "MobTank", "MobRapide", "Mob"],
}


def _types_pour_continent(continent):
    cle = str(continent).lower().strip()
    return TYPES_PAR_CONTINENT.get(cle, TYPES_PAR_CONTINENT["pirate"])


def _faire_groupe(type_mob, nombre, decalage, bonus_vitesse):
    return {
        "type": type_mob,
        "nombre": int(max(1, nombre)),
        "decalage": round(float(max(0.0, decalage)), 2),
        "bonus_vitesse": round(float(max(0.0, bonus_vitesse)), 2),
    }


def _generer_groupes(continent, niveau, numero_vague):
    """
    Génère les groupes de mobs pour une vague donnée.

    Progression cible (mobs totaux, hors boss) :
        Niveau 1 : V1≈9   V2≈13  V3≈17
        Niveau 2 : V1≈21  V2≈30  V3≈39
        Niveau 3 : V1≈42  V2≈54  V3≈66
        Niveau 4 : V1≈65  V2≈80  V3≈95
        Niveau 5 : V1≈90  V2≈100 V3≈100 (plafonné)
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
    # Intervalle de spawn : plus espacé au niveau 1 pour laisser le temps de réagir
    intervalle = 1.1 - (niveau * 0.04) - (numero_vague * 0.04)
    intervalle = max(0.35, intervalle)
    return {
        "intervalle_spawn": round(intervalle, 2),
        "groupes": _generer_groupes(continent, niveau, numero_vague),
        "commentaire": "Progression calibree : ~9 mobs niveau 1 vague 1, ~100 mobs niveau 5.",
    }


def charger_configuration(continent, niveau):
    niveau_int = int(max(1, niveau))
    return {
        1: _generer_vague(continent, niveau_int, 1),
        2: _generer_vague(continent, niveau_int, 2),
        3: _generer_vague(continent, niveau_int, 3),
        4: _generer_vague(continent, niveau_int, 4),
    }