import pygame
from setting import largeur_ecran, hauteur_ecran, FPS
from menu import Menu
from game import Jeu


def main():
    pygame.init()
    ecran = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
    pygame.display.set_caption("Abyssal Raiders")
    horloge = pygame.time.Clock()

    menu = Menu(ecran)
    etat_application = "menu"

    while etat_application != "quitter":
        delta_temps = horloge.tick(FPS) / 1000

        if etat_application == "menu":
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT: 
                    etat_application = "quitter"
                else:
                    resultat = menu.gerer_evenement(evenement)
                    if resultat == "lancer_jeu":
                        etat_application = "jeu"
                    elif resultat == "quitter":
                        etat_application = "quitter"

            menu.mise_a_jour(delta_temps)
            menu.dessiner()
            pygame.display.flip()

        elif etat_application == "jeu":
            jeu = Jeu(menu.monde_selectionne, menu.volume_son, menu.niveau_selectionne)
            jeu.lancer()
            etat_application = "quitter"

    pygame.quit()


if __name__ == "__main__":
    main()