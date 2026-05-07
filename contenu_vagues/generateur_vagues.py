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
    types = _types_pour_continent(continent)
    groupes = []
    base_niveau = 10 + (niveau - 1) * 2
    base_vague = 2 + (numero_vague - 1) * 2
    decalage = 0.0
    for index in range(6):
        type_mob = types[(index + niveau + numero_vague) % len(types)]
        nombre = base_niveau + base_vague + index
        bonus_vitesse = 0.01 * ((niveau + numero_vague + index) % 9)
        groupes.append(_faire_groupe(type_mob, nombre, decalage, bonus_vitesse))
        decalage += 0.45
    return groupes


def _generer_vague(continent, niveau, numero_vague):
    intervalle = 0.92 - (niveau * 0.02) - (numero_vague * 0.05)
    intervalle = max(0.2, intervalle)
    return {
        "intervalle_spawn": round(intervalle, 2),
        "groupes": _generer_groupes(continent, niveau, numero_vague),
        "commentaire": "Progression equilibree avec alternance d archetypes.",
    }


def charger_configuration(continent, niveau):
    niveau_int = int(max(1, niveau))
    return {
        1: _generer_vague(continent, niveau_int, 1),
        2: _generer_vague(continent, niveau_int, 2),
        3: _generer_vague(continent, niveau_int, 3),
        4: _generer_vague(continent, niveau_int, 4),
    }
