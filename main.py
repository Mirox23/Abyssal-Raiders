"""
Qu'est-ce que le fichier gère : Ce fichier gère la partie main du projet.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Résultat : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import pygame
from setting import largeur_ecran, hauteur_ecran, FPS
from menu import Menu
from jeu import Jeu
from musique import MusiqueManager
from dialogue_quitter_sauvegarde import demander_sauvegarde_avant_quitter
from progression_monde import ProgressionMonde


def main():
    """
    Explication de ce que fais la fonction : Cette fonction exécute main.
    Les entrées : Cette fonction ne demande pas de paramètre direct.
    Le résultat : Retourne la valeur attendue ou applique l'action prévue.
    """
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    ecran = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
    pygame.display.set_caption("Abyssal Raiders")
    horloge = pygame.time.Clock()

    menu = Menu(ecran)
    progression_monde = ProgressionMonde()
    etat_application = "menu"

    while etat_application != "quitter":
        delta_temps = horloge.tick(FPS) / 1000

        if etat_application == "menu":
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    if demander_sauvegarde_avant_quitter(ecran, progression_monde):
                        etat_application = "quitter"
                else:
                    resultat = menu.gerer_evenement(evenement)
                    if resultat == "lancer_jeu":
                        etat_application = "jeu"
                    elif resultat == "quitter":
                        if demander_sauvegarde_avant_quitter(ecran, progression_monde):
                            etat_application = "quitter"

            menu.mise_a_jour(delta_temps)
            ecran.fill((0, 0, 0))
            menu.dessiner()
            pygame.display.flip()

        elif etat_application == "jeu":
            jeu = Jeu(menu.monde_selectionne, menu.volume_son, menu.niveau_selectionne, progression_monde)
            resultat = jeu.lancer()
            if resultat.get("quitter"):
                if demander_sauvegarde_avant_quitter(ecran, progression_monde):
                    etat_application = "quitter"
                else:
                    etat_application = "menu"
                continue
            menu.relancer_musique_menu()
            menu.appliquer_progression(progression_monde)
            if resultat.get("ouvrir_map"):
                menu.etat = "map"
            etat_application = "menu"

    pygame.quit()
 

if __name__ == "__main__":
    main()
