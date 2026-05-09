"""
Qu'est-ce que le fichier gère : Ce fichier gère la partie sauvegarde injecter progression du projet.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Résultat : Des comportements, calculs ou affichages utilisés par le jeu.
"""


def _aligner_liste_niveaux(liste_en_entree):
    """
    Explication de ce que fais la fonction : Cette fonction exécute aligner liste niveaux.
    Les entrées : liste_en_entree.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
    if isinstance(liste_en_entree, list) is False:
        liste_en_entree = []
    resultat = liste_en_entree + [False] * 8
    huit = resultat[:8]
    return huit


def _aligner_ligne_vagues(ligne):
    """
    Explication de ce que fais la fonction : Cette fonction exécute aligner ligne vagues.
    Les entrées : ligne.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
    ligne_ok = list(ligne) if isinstance(ligne, list) else [False, False, False, False]
    complete = ligne_ok + [False, False, False, False]
    quatre = complete[:4]
    return quatre


def copier_donnees_dans_progression(donnees, progression_monde):
    """
    Explication de ce que fais la fonction : Cette fonction exécute copier donnees dans progression.
    Les entrées : donnees, progression_monde.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
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
                for ligne in liste_niveaux[:7]:  # 7 niveaux maintenant
                    propre.append(_aligner_ligne_vagues(ligne))
            while len(propre) < 7:  # 7 niveaux maintenant
                propre.append([False, False, False, False])
            progression_monde.succes_vagues[continent] = propre

    nv = donnees.get("niveau_joueur", 1)
    return nv
