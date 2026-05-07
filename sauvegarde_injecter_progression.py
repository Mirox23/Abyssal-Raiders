"""
Quand on charge une partie, on recopie les infos dans ProgressionMonde.
La logique est la même qu'avant, juste déplacée ici.
"""


def _aligner_liste_niveaux(liste_en_entree):
    if isinstance(liste_en_entree, list) is False:
        liste_en_entree = []
    resultat = liste_en_entree + [False] * 8
    huit = resultat[:8]
    return huit


def _aligner_ligne_vagues(ligne):
    ligne_ok = list(ligne) if isinstance(ligne, list) else [False, False, False, False]
    complete = ligne_ok + [False, False, False, False]
    quatre = complete[:4]
    return quatre


def copier_donnees_dans_progression(donnees, progression_monde):
    if donnees is None:
        return 1

    niveaux = donnees.get("niveaux_conquis", {})
    for continent, liste in niveaux.items():
        if continent in progression_monde.niveaux_conquis:
            progression_monde.niveaux_conquis[continent] = _aligner_liste_niveaux(liste)

    succes_brut = donnees.get("succès_vagues", {})
    for continent, liste_niveaux in succes_brut.items():
        if continent in progression_monde.succes_vagues:
            propre = []
            if isinstance(liste_niveaux, list):
                for ligne in liste_niveaux[:8]:
                    propre.append(_aligner_ligne_vagues(ligne))
            while len(propre) < 8:
                propre.append([False, False, False, False])
            progression_monde.succes_vagues[continent] = propre

    nv = donnees.get("niveau_joueur", 1)
    return nv
