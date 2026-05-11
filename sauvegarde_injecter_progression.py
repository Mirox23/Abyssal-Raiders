"""
A quoi sert le fichier : Ce fichier gère l'injection des données de sauvegarde dans l'objet de progression du monde. Il s'assure que les données chargées sont correctement formatées et alignées avec la structure attendue par le jeu, en gérant les cas où les anciennes sauvegardes peuvent avoir des structures différentes. Il convertit et nettoie les données pour garantir la compatibilité entre les versions.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu.
"""


def _aligner_liste_niveaux(liste_en_entree):
    """
    A quoi sert la fonction : S'assure que la liste des niveaux a exactement 8 éléments en ajoutant des valeurs False si nécessaire pour garantir la compatibilité.
    Entrée : liste_en_entree (la liste de niveaux à aligner, peut être vide ou incomplète).
    Sortie : Retourne une liste de 8 éléments avec les valeurs d'origine complétées par False.
    """
    if isinstance(liste_en_entree, list) is False:
        liste_en_entree = []
    resultat = liste_en_entree + [False] * 8
    huit = resultat[:8]
    return huit


def _aligner_ligne_vagues(ligne):
    """
    A quoi sert la fonction : S'assure que la ligne de vagues a exactement 4 éléments en ajoutant des valeurs False si nécessaire pour maintenir la cohérence des données.
    Entrée : ligne (la ligne de vagues à aligner, peut être vide ou incomplète).
    Sortie : Retourne une liste de 4 éléments avec les valeurs d'origine complétées par False.
    """
    ligne_ok = list(ligne) if isinstance(ligne, list) else [False, False, False, False]
    complete = ligne_ok + [False, False, False, False]
    quatre = complete[:4]
    return quatre


def copier_donnees_dans_progression(donnees, progression_monde):
    """
    A quoi sert la fonction : Copie les données de sauvegarde dans l'objet de progression du monde en s'assurant que tous les niveaux et succès sont correctement formatés et alignés.
    Entrée : donnees (le dictionnaire contenant les données de sauvegarde à injecter), progression_monde (l'objet de progression du monde à mettre à jour).
    Sortie : Retourne le niveau du joueur depuis les données de sauvegarde, ou 1 si les données sont invalides.
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
