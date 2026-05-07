import pygame
from setting import largeur_ecran, hauteur_ecran


# Toutes les etapes du tutoriel dans l'ordre
etape_tourelle = 0
etape_placer_tour = 1
etape_lancer_vague = 2
etape_ameliorer_tour = 3
etape_infos_ameliorer = 4
etape_modification = 5
etape_succes = 6
etape_recompense = 7
etape_arbre_talent = 8
etape_competence = 9
etape_objet = 10
etape_termine = 11

# Le seuil d'or a partir duquel on suggere d'ameliorer une tour
argent_seuil_amelioration = 15

# Les messages affiches a chaque etape
messages_etapes = {
    etape_tourelle: "Ouvrez le telephone puis cliquez sur 'Tourelle' pour placer votre premiere defense !",
    etape_placer_tour: "Choisissez une tour puis cliquez sur la carte pour la poser.",
    etape_lancer_vague: "Bien ! Maintenant ouvrez le telephone et cliquez sur 'New vague' pour lancer la premiere vague.",
    etape_ameliorer_tour: "Vous avez assez d'or ! Cliquez sur une de vos tours pour la selectionner.",
    etape_infos_ameliorer: "Maintenant ouvrez le telephone, allez dans 'Info' pour ameliorer votre tour !",
    etape_modification: "Vague terminee ! Cliquez sur 'Modification' dans l'ecran de fin pour reamenager vos defenses.",
    etape_succes: "Vous aurez ici votre parcours de completaison du jeu. Allez voir vos succes dans le telephone !",
    etape_recompense: "Cliquez sur le bouton 'Recompenses - Talents' en haut a droite pour voir vos recompenses.",
    etape_arbre_talent: "Vous etes dans les recompenses. Allez dans l'onglet 'Arbre a talents' pour ameliorer vos skills !",
    etape_competence: "Voici vos competences et objets qui vous permettront de vous sortir d'une mort certaine. Ouvrez 'Competence' dans le telephone.",
    etape_objet: "Maintenant ouvrez 'Objets' dans le telephone pour voir votre inventaire.",
    etape_termine: "",
}


class GestionnaireTutoriel:
    def __init__(self):
        self.etape_actuelle = etape_tourelle
        self.actif = True
        self.police_message = pygame.font.SysFont("consolas", 15, bold=True)
        self.police_titre = pygame.font.SysFont("consolas", 13)
        self.timer_clignotement = 0.0
        self.fleche_visible = True

    def est_termine(self):
        return self.etape_actuelle >= etape_termine

    def passer_etape(self):
        if self.etape_actuelle < etape_termine:
            self.etape_actuelle += 1

    def notifier_action(self, nom_action):
        """
        Appele depuis game.py a chaque action du joueur.
        nom_action : chaine qui decrit ce que le joueur vient de faire.
        """
        if not self.actif or self.est_termine():
            return

        if self.etape_actuelle == etape_tourelle:
            if nom_action == "telephone_tourelle_clique":
                self.passer_etape()

        elif self.etape_actuelle == etape_placer_tour:
            if nom_action == "tour_placee":
                self.passer_etape()

        elif self.etape_actuelle == etape_lancer_vague:
            if nom_action == "vague_lancee":
                self.passer_etape()

        elif self.etape_actuelle == etape_ameliorer_tour:
            if nom_action == "tour_selectionnee":
                self.passer_etape()

        elif self.etape_actuelle == etape_infos_ameliorer:
            if nom_action == "telephone_info_clique":
                self.passer_etape()

        elif self.etape_actuelle == etape_modification:
            # Le joueur clique sur le bouton Modification deja visible a l'ecran
            if nom_action == "modification_cliquee":
                self.passer_etape()

        elif self.etape_actuelle == etape_succes:
            if nom_action == "telephone_succes_clique":
                self.passer_etape()

        elif self.etape_actuelle == etape_recompense:
            if nom_action == "bouton_recompense_clique":
                self.passer_etape()

        elif self.etape_actuelle == etape_arbre_talent:
            if nom_action == "onglet_talent_clique":
                self.passer_etape()

        elif self.etape_actuelle == etape_competence:
            if nom_action == "telephone_competence_clique":
                self.passer_etape()

        elif self.etape_actuelle == etape_objet:
            if nom_action == "telephone_objet_clique":
                self.passer_etape()

    def notifier_vague_terminee(self):
        """
        Appele depuis game.py quand la vague se termine.
        On passe directement a l'etape modification : le message apparait
        tout seul sur l'ecran de fin de vague, sans ouvrir le telephone.
        """
        if not self.actif or self.est_termine():
            return
        if self.etape_actuelle == etape_infos_ameliorer or self.etape_actuelle == etape_ameliorer_tour:
            self.etape_actuelle = etape_modification

    def mettre_a_jour(self, delta_temps):
        if not self.actif or self.est_termine():
            return
        self.timer_clignotement += delta_temps
        if self.timer_clignotement >= 0.6:
            self.timer_clignotement = 0.0
            self.fleche_visible = not self.fleche_visible

    def dessiner(self, fenetre):
        if not self.actif or self.est_termine():
            return

        message = messages_etapes.get(self.etape_actuelle, "")
        if not message:
            return

        largeur_panneau = min(largeur_ecran - 40, 700)
        hauteur_panneau = 72
        x_panneau = largeur_ecran // 2 - largeur_panneau // 2
        y_panneau = hauteur_ecran - hauteur_panneau - 16

        # Fond semi-transparent
        surface_fond = pygame.Surface((largeur_panneau, hauteur_panneau), pygame.SRCALPHA)
        surface_fond.fill((10, 14, 28, 210))
        fenetre.blit(surface_fond, (x_panneau, y_panneau))

        # Bordure coloree selon la phase du tutoriel
        couleur_bordure = _couleur_etape(self.etape_actuelle)
        pygame.draw.rect(
            fenetre,
            couleur_bordure,
            pygame.Rect(x_panneau, y_panneau, largeur_panneau, hauteur_panneau),
            width=2,
            border_radius=8
        )

        # Titre avec le numero d'etape
        numero_etape = min(self.etape_actuelle + 1, etape_termine)
        texte_titre = f"Tutoriel - Etape {numero_etape} / {etape_termine}"
        surface_titre = self.police_titre.render(texte_titre, True, couleur_bordure)
        fenetre.blit(surface_titre, (x_panneau + 12, y_panneau + 8))

        # Message principal coupe en deux lignes si besoin
        lignes = _decouper_message(message, self.police_message, largeur_panneau - 30)
        for i, ligne in enumerate(lignes):
            surface_ligne = self.police_message.render(ligne, True, (240, 245, 255))
            fenetre.blit(surface_ligne, (x_panneau + 12, y_panneau + 28 + i * 18))

        # Fleche clignotante vers l'element concerne
        if self.fleche_visible:
            _dessiner_fleche_indicatrice(fenetre, self.etape_actuelle)


def _couleur_etape(etape):
    """Retourne une couleur differente selon la phase du tutoriel."""
    if etape <= etape_lancer_vague:
        return (80, 200, 120)
    if etape <= etape_modification:
        return (80, 160, 240)
    if etape <= etape_arbre_talent:
        return (220, 180, 60)
    return (200, 120, 240)


def _decouper_message(message, police, largeur_max):
    """Coupe un message en plusieurs lignes pour qu'il tienne dans la largeur."""
    mots = message.split(" ")
    lignes = []
    ligne_courante = ""
    for mot in mots:
        test = ligne_courante + (" " if ligne_courante else "") + mot
        largeur_test = police.size(test)[0]
        if largeur_test <= largeur_max:
            ligne_courante = test
        else:
            if ligne_courante:
                lignes.append(ligne_courante)
            ligne_courante = mot
    if ligne_courante:
        lignes.append(ligne_courante)
    return lignes[:2]


def _dessiner_fleche_indicatrice(fenetre, etape):
    """
    Dessine une petite fleche qui pointe vers l'element concerne par l'etape.
    """
    # Par defaut on pointe vers le telephone en bas a droite
    cible_x = largeur_ecran - 105
    cible_y = hauteur_ecran - 70

    # Pour les etapes liees au bouton recompense en haut a droite
    if etape == etape_recompense or etape == etape_arbre_talent:
        cible_x = largeur_ecran - 110
        cible_y = 34

    # Pour l'etape modification le bouton est au centre de l'ecran
    if etape == etape_modification:
        cible_x = largeur_ecran // 2 + 120
        cible_y = hauteur_ecran // 2 + 110

    taille_fleche = 10
    couleur = (255, 240, 80)

    point_haut = (cible_x, cible_y - 28)
    point_bas_gauche = (cible_x - taille_fleche, cible_y - 28 - taille_fleche)
    point_bas_droit = (cible_x + taille_fleche, cible_y - 28 - taille_fleche)

    pygame.draw.polygon(fenetre, couleur, [point_haut, point_bas_gauche, point_bas_droit])
    pygame.draw.polygon(fenetre, (200, 160, 20), [point_haut, point_bas_gauche, point_bas_droit], width=1)