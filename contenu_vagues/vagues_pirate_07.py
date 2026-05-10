"""
A quoi sert le fichier : Ce fichier contient la configuration des vagues pour le monde pirate niveau 7. Il charge automatiquement les vagues 1 à 4 depuis le générateur de vagues, ce qui permet de définir les ennemis, leur nombre, leur timing et leurs caractéristiques pour chaque vague de ce niveau spécifique.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu.
"""

# Importe le chargeur de configuration depuis le générateur de vagues
from contenu_vagues.generateur_vagues import charger_configuration as _charger_configuration

# Charge la configuration des vagues pour le monde pirate niveau 7
CONFIGURATION_VAGUES = _charger_configuration("pirate", 7)
