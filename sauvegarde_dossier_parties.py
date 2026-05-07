import os


DOSSIER_SAUVEGARDES = "sauvegardes"


def assurer_le_dossier():
    if not os.path.exists(DOSSIER_SAUVEGARDES):
        os.makedirs(DOSSIER_SAUVEGARDES, exist_ok=True)
