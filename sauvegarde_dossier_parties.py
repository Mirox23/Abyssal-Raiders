import os


DOSSIER_SAUVEGARDES = "sauvegardes"


def assurer_le_dossier():
    """
    Explication de ce que fais la fonction : Cette fonction exécute assurer le dossier.
    Les entrées : Cette fonction ne demande pas de paramètre direct.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
    if not os.path.exists(DOSSIER_SAUVEGARDES):
        os.makedirs(DOSSIER_SAUVEGARDES, exist_ok=True)



