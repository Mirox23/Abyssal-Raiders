"""
A quoi sert le fichier : Ce fichier est le point d'entrée principal du jeu. Il initialise Pygame, gère la boucle principale du jeu et fait la navigation entre le menu principal et le jeu. Il s'occupe aussi de la gestion des événements comme la fermeture de la fenêtre et le passage entre les différents états de l'application.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Sortie : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import pygame
from setting import largeur_ecran, hauteur_ecran, FPS
from menu import Menu
from jeu import Jeu
from dialogue_quitter_sauvegarde import demander_sauvegarde_avant_quitter
from progression_monde import ProgressionMonde


def main():
    """
    A quoi sert la fonction : Fonction principale qui démarre le jeu et gère la boucle principale de l'application.
    Entrée : Cette fonction ne demande pas de paramètre direct.
    Sortie : Retourne la valeur attendue ou applique l'action prévue.
    """
    # Initialisation de Pygame avec configuration audio optimisée
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    
    # Création de la fenêtre de jeu
    ecran = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
    pygame.display.set_caption("Abyssal Raiders")
    horloge = pygame.time.Clock()

    # Création des objets principaux du jeu
    menu = Menu(ecran)
    progression_monde = ProgressionMonde()
    etat_application = "menu"  # État initial : on commence au menu

    # Boucle principale du jeu qui tourne tant qu'on ne quitte pas
    while etat_application != "quitter":
        delta_temps = horloge.tick(FPS) / 1000  # Temps écoulé depuis la dernière frame

        # Gestion du menu principal
        if etat_application == "menu":
            # Gestion des événements (clics, fermeture, etc.)
            for evenement in pygame.event.get():
                if evenement.type == pygame.QUIT:  # Clic sur la croix pour fermer
                    if demander_sauvegarde_avant_quitter(ecran, progression_monde):
                        etat_application = "quitter"
                else:
                    resultat = menu.gerer_evenement(evenement)
                    # Changement d'état selon l'action dans le menu
                    if resultat == "lancer_jeu":
                        etat_application = "jeu"
                    elif resultat == "quitter":
                        if demander_sauvegarde_avant_quitter(ecran, progression_monde):
                            etat_application = "quitter"

            # Mise à jour et affichage du menu
            menu.mise_a_jour(delta_temps)
            ecran.fill((0, 0, 0))  # Effacer l'écran en noir
            menu.dessiner()
            pygame.display.flip()  # Afficher le nouveau contenu

        # Lancement du jeu
        elif etat_application == "jeu":
            # Création d'une nouvelle instance de jeu avec les paramètres choisis
            jeu = Jeu(menu.monde_selectionne, menu.volume_son, menu.niveau_selectionne, progression_monde)
            resultat = jeu.lancer()
            
            # Gestion du retour au menu ou de la fermeture
            if resultat.get("quitter"):
                if demander_sauvegarde_avant_quitter(ecran, progression_monde):
                    etat_application = "quitter"
                else:
                    etat_application = "menu"
                continue  # Recommence la boucle avec le nouvel état
            
            # Remise en état du menu après la partie
            menu.relancer_musique_menu()
            menu.appliquer_progression(progression_monde)
            if resultat.get("ouvrir_map"):
                menu.etat = "map"
            etat_application = "menu"

    # Fermeture propre de Pygame
    pygame.quit()
 

# Point d'entrée du programme - lance la fonction main si on exécute ce fichier
if __name__ == "__main__":
    main()
