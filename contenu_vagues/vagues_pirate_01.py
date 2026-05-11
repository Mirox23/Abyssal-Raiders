"""
A quoi sert le fichier : Ce fichier contient la configuration des vagues pour le monde pirate au niveau 1. Il utilise le générateur partagé pour créer les quatre vagues de ce palier en définissant les types d'ennemis, quantités, délais d'apparition et autres paramètres. Le moteur de jeu lit ensuite la constante CONFIGURATION_VAGUES pour enchaîner les vagues.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu.
"""

# On récupère la fonction du générateur (même logique pour tous les mondes)
from contenu_vagues.generateur_vagues import charger_configuration as _charger_configuration

# Charge la configuration des vagues pour le monde pirate niveau 1
CONFIGURATION_VAGUES = _charger_configuration("pirate", 1)
