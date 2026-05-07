from datetime import datetime


def _copie_niveaux_conquis(progression_monde):
    resultat = {}
    if progression_monde is None:
        return resultat
    for continent, liste in progression_monde.niveaux_conquis.items():
        resultat[continent] = list(liste)
    return resultat


def _copie_succes_vagues(progression_monde):
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
