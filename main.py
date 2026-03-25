# point d'entrée du jeu, c'est là qu'on lance la boucle principale (le jeu)

from game import Jeu

if __name__ == "__main__":
    jeu = Jeu()
    jeu.lancer()