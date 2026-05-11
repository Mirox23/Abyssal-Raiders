"""
A quoi sert le fichier : Ce fichier sert de module d'importation central pour tous les panneaux d'interface utilisateur du jeu. Il regroupe et exporte les classes des panneaux comme les fenêtres de récompenses de talents, les panneaux de compétences, les panneaux d'objets et les panneaux de paramètres musicaux pour faciliter leur utilisation dans les autres parties du jeu.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu.
"""

from fenetre_recompenses_talents import FenetreRecompensesTalents
from panneau_competences import PanneauCompetences
from panneau_objets import PanneauObjets
from panneau_parametres_musique import PanneauParametresMusique

__all__ = [
    'FenetreRecompensesTalents',
    'PanneauCompetences',
    'PanneauObjets',
    'PanneauParametresMusique',
]
