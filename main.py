import pygame
from setting import largeur_ecran, hauteur_ecran, FPS
from menu import Menu
from game import Jeu


def main():
    pygame.init()
    ecran = pygame.display.set_mode((largeur_ecran, hauteur_ecran)) #initialisation de la fenêtre du jeu avec les dimensions définies dans setting.py
    pygame.display.set_caption("Abyssal Raiders")
    horloge = pygame.time.Clock()

    menu = Menu(ecran)
    etat_application = "menu"

    while etat_application != "quitter": #tant que le joueur n'a pas choisi de quitter le jeu, on reste dans la boucle principale qui gère les différents états de l'application (menu, jeu, etc.)
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

            menu.mise_a_jour(delta_temps) #met à jour les éléments du menu (animations, etc.) en fonction du temps écoulé depuis la dernière mise à jour pour que les animations soient fluides et indépendantes du nombre de frames par seconde
            menu.dessiner()
            pygame.display.flip()

        elif etat_application == "jeu":
            jeu = Jeu()
            jeu.lancer()
            etat_application = "quitter"

    pygame.quit()


if __name__ == "__main__":
    main()