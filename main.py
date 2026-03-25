# point d'entrée — gère le menu puis lance le jeu

import pygame
from setting import largeur_ecran, hauteur_ecran, FPS
from menu import Menu
from game import Jeu


def main():
    pygame.init()
    ecran   = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
    pygame.display.set_caption("Abyssal Raiders")
    horloge = pygame.time.Clock()

    menu = Menu(ecran)
    etat = "menu"   # "menu" | "jeu" | "quitter"

    while etat != "quitter":
        dt = horloge.tick(FPS) / 1000

        if etat == "menu":
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:
                    etat = "quitter"
                else:
                    resultat = menu.gerer_evenement(evenement)
                    if resultat == "jouer":
                        etat = "jeu"
                    elif resultat == "quitter":
                        etat = "quitter"

            menu.mise_a_jour(dt)
            menu.dessiner()
            pygame.display.flip()

        elif etat == "jeu":
            # Le Jeu gère sa propre boucle interne ; quand elle se termine
            # on revient au menu.
            jeu = Jeu()
            jeu.lancer()          # bloquant jusqu'à fermeture de la fenêtre
            etat = "quitter"      # après la partie on quitte proprement

    pygame.quit()


if __name__ == "__main__":
    main()