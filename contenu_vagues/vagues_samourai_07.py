"""
À quoi sert le fichier : Ici on n'expose que la configuration des vagues
    pour le monde samouraï, pour le niveau 7 du jeu. Le fichier appelle le
    générateur partagé pour remplir CONFIGURATION_VAGUES : types
    d'ennemis, quantités, délais entre les apparitions, etc. Comme ça le
    moteur lit une seule constante claire.

Entrée : Rien n'est passé en paramètre à l'import : le continent et le
    numéro de niveau sont déjà choisis dans le nom du fichier.

Sortie : La variable CONFIGURATION_VAGUES, un dictionnaire que le jeu
    utilise pour enchaîner les quatre vagues de ce palier.
"""

# On récupère la fonction du générateur (même logique pour tous les mondes)
from contenu_vagues.generateur_vagues import charger_configuration as _charger_configuration

# Charge la configuration des vagues pour le monde samouraï niveau 7
CONFIGURATION_VAGUES = _charger_configuration("samourai", 7)
