"""
Qu'est-ce que le fichier gère : Ce fichier gère la partie fenetre arbre talents du projet.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Résultat : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import os
import pygame
import unicodedata
from decoration_cadre_abysse import dessiner_cadre_panneau
from interface import Bouton
from setting import largeur_ecran, hauteur_ecran

class FenetreArbreTalents:
    """
    Arbre à talents avec icônes PNG (dossier image/talent/).
    L'arbre se reset à chaque nouveau niveau de jeu, mais le joueur
    repart avec un petit bonus permanent basé sur son niveau précédent.
    """

    TALENTS = {
        "degats_competence": {
            "nom": "Poudre noire +",
            "icone": "image/talent/poudre_noire.png",
            "max": 4,
            "desc_courte": "+2 dégâts par compétence",
            "desc_longue": "Chaque niveau ajoute +2 dégâts\nà toutes vos compétences actives.",
        },
        "reduction_cout": {
            "nom": "Marchandage pirate",
            "icone": "image/talent/marchandage.png",
            "max": 3,
            "desc_courte": "-1 coût par compétence",
            "desc_longue": "Réduit de 1 or le coût\nde chaque compétence utilisée.",
        },
        "chasseur": {
            "nom": "Chasseur de prime",
            "icone": "image/talent/chasseur.png",
            "max": 3,
            "desc_courte": "+1 or bonus mobs rapides",
            "desc_longue": "Les mobs rapides et kamikazes\nvous rapportent +1 or à la mort.",
        },
        "ingenieur": {
            "nom": "Ingénieur de guilde",
            "icone": "image/talent/ingenieur.png",
            "max": 3,
            "desc_courte": "+8 portée à toutes les tours",
            "desc_longue": "Chaque niveau augmente\nla portée de toutes vos tours de 8.",
        },
        "resistance_mur": {
            "nom": "Mur renforcé",
            "icone": "image/talent/mur_renforce.png",
            "max": 3,
            "desc_courte": "-1 dégât reçu par le mur",
            "desc_longue": "Le mur absorbe 1 dégât\nde plus par niveau de talent.",
        },
        "alchimiste": {
            "nom": "Alchimiste fou",
            "icone": "image/talent/alchimiste.png",
            "max": 2,
            "desc_courte": "Effets des objets ×1.5",
            "desc_longue": "Tous vos objets (potions,\nbourses…) ont un effet amplifié.",
        },
    }

    def __init__(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute init.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        self.visible = False
        self.rect = pygame.Rect(120, 60, 760, 470)
        self.police_titre = pygame.font.SysFont("consolas", 22, bold=True)
        self.police_nom = pygame.font.SysFont("consolas", 13, bold=True)
        self.police_desc = pygame.font.SysFont("consolas", 11)
        self.police_niv = pygame.font.SysFont("consolas", 12)
        self.bouton_fermer = Bouton(self.rect.right - 100, self.rect.y + 12, 84, 30, "Fermer", 14)

        # État des talents : niveau actuel pour chaque talent
        self.talents = {}
        for cle, donnees_talent in self.TALENTS.items():
            self.talents[cle] = {"niveau": 0, "max": donnees_talent["max"]}

        # Icônes chargées une seule fois
        self._icones = {}
        self._charger_icones()

        self._boutons_talents = []
        self._maj_boutons()

    def _charger_icones(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute charger icones.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        taille = (48, 48)
        for cle, donnees in self.TALENTS.items():
            chemin = self._trouver_chemin_icone(cle, donnees["icone"])
            if os.path.exists(chemin):
                try:
                    img = pygame.image.load(chemin).convert_alpha()
                    self._icones[cle] = pygame.transform.smoothscale(img, taille)
                except Exception:
                    self._icones[cle] = None
            else:
                self._icones[cle] = None

    def _normaliser_nom(self, texte):
        """
        Explication de ce que fais la fonction : Cette fonction exécute normaliser nom.
        Les entrées : texte.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        texte_normalise = unicodedata.normalize("NFKD", texte)
        texte_sans_accents = "".join(
            caractere for caractere in texte_normalise if not unicodedata.combining(caractere)
        )
        return texte_sans_accents.lower().replace(" ", "_")

    def _trouver_chemin_icone(self, cle_talent, chemin_par_defaut):
        """
        Explication de ce que fais la fonction : Cette fonction exécute trouver chemin icone.
        Les entrées : cle_talent, chemin_par_defaut.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        chemins_possibles = [
            chemin_par_defaut,
            f"image/talent/{cle_talent}.png",
            f"image/talent/{cle_talent}.jpg",
            f"image/talent/{cle_talent}.jpeg",
            f"image/talent/{cle_talent}.webp",
        ]

        for chemin_actuel in chemins_possibles:
            if os.path.exists(chemin_actuel):
                return chemin_actuel

        dossier_talent = "image/talent"
        if not os.path.isdir(dossier_talent):
            return chemin_par_defaut

        cle_normalisee = self._normaliser_nom(cle_talent)
        nom_talent = self.TALENTS[cle_talent]["nom"]
        nom_talent_normalise = self._normaliser_nom(nom_talent)

        for nom_fichier in os.listdir(dossier_talent):
            base_sans_extension = os.path.splitext(nom_fichier)[0]
            base_normalisee = self._normaliser_nom(base_sans_extension)
            if cle_normalisee in base_normalisee or nom_talent_normalise in base_normalisee:
                return os.path.join(dossier_talent, nom_fichier)

        return chemin_par_defaut

    def _maj_boutons(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute maj boutons.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        self._boutons_talents = []
        cols = 3
        larg_carte = 220
        haut_carte = 130
        marge_x = 18
        marge_y = 14
        depart_x = self.rect.x + 20
        depart_y = self.rect.y + 80

        for i, cle in enumerate(self.TALENTS):
            col = i % cols
            lig = i // cols
            bx = depart_x + col * (larg_carte + marge_x)
            by = depart_y + lig * (haut_carte + marge_y)
            self._boutons_talents.append((cle, pygame.Rect(bx, by, larg_carte, haut_carte)))

    def ouvrir(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute ouvrir.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        self.visible = True

    def reset_pour_nouveau_niveau(self, niveau_joueur_avant):
        """
        Explication de ce que fais la fonction : Cette fonction exécute reset pour nouveau niveau.
        Les entrées : niveau_joueur_avant.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        for cle in self.talents:
            self.talents[cle]["niveau"] = 0
        # bonus permanent : +1 degats tous les 4 niveaux, +1 portée tous les 5 niveaux
        bonus_degats = niveau_joueur_avant // 4
        bonus_portee = niveau_joueur_avant // 5
        return bonus_degats, bonus_portee

    def gerer_clic(self, pos_clic, progression):
        """
        Explication de ce que fais la fonction : Cette fonction gère gerer clic en fonction du contexte courant.
        Les entrées : pos_clic, progression.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if not self.visible:
            return None
        if self.bouton_fermer.rect.collidepoint(pos_clic):
            self.visible = False
            return ("fermer", None)
        for cle, rect in self._boutons_talents:
            t = self.talents[cle]
            if rect.collidepoint(pos_clic):
                if progression.points_talent > 0 and t["niveau"] < t["max"]:
                    progression.points_talent -= 1
                    t["niveau"] += 1
                    return ("talent", cle)
        if self.rect.collidepoint(pos_clic):
            return ("consomme", None)
        return None

    def dessiner(self, fenetre, progression):
        """
        Explication de ce que fais la fonction : Cette fonction dessine dessiner à l'écran.
        Les entrées : fenetre, progression.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if not self.visible:
            return

        voile = pygame.Surface((largeur_ecran, hauteur_ecran), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 150))
        fenetre.blit(voile, (0, 0))

        dessiner_cadre_panneau(fenetre, self.rect)

        titre = self.police_titre.render("Arbre à talents", True, (238, 218, 182))
        fenetre.blit(titre, (self.rect.x + 14, self.rect.y + 14))

        pts_txt = self.police_desc.render(
            f"Points disponibles : {progression.points_talent}  —  Bonus permanent : +{progression.bonus_degats_permanent} dégâts / +{progression.bonus_portee_permanent} portée",
            True, (245, 205, 140)
        )
        fenetre.blit(pts_txt, (self.rect.x + 14, self.rect.y + 44))
        self.bouton_fermer.dessiner(fenetre)

        for cle, rect in self._boutons_talents:
            t = self.talents[cle]
            info = self.TALENTS[cle]
            peut = progression.points_talent > 0 and t["niveau"] < t["max"]
            maximal = t["niveau"] >= t["max"]

            # Fond de la carte
            coul_fond = (56, 43, 31)
            coul_bord = (214, 177, 108) if maximal else (143, 176, 111) if peut else (118, 93, 65)
            pygame.draw.rect(fenetre, coul_fond, rect, border_radius=10)
            pygame.draw.rect(fenetre, coul_bord, rect, width=2 if (peut or maximal) else 1, border_radius=10)

            # Icône
            icone = self._icones.get(cle)
            if icone:
                fenetre.blit(icone, (rect.x + 8, rect.y + 8))
                tx = rect.x + 64
            else:
                # Carré de couleur de remplacement si pas d'icône
                pygame.draw.rect(fenetre, (80, 60, 40), pygame.Rect(rect.x + 8, rect.y + 8, 48, 48), border_radius=6)
                tx = rect.x + 64

            # Nom du talent
            surf_nom = self.police_nom.render(info["nom"], True, (245, 229, 194))
            fenetre.blit(surf_nom, (tx, rect.y + 10))

            # Description courte
            surf_desc = self.police_desc.render(info["desc_courte"], True, (205, 184, 151))
            fenetre.blit(surf_desc, (tx, rect.y + 28))

            # Description longue (2 lignes)
            lignes = info["desc_longue"].split("\n")
            for j, ligne in enumerate(lignes):
                s = self.police_desc.render(ligne, True, (169, 145, 119))
                fenetre.blit(s, (rect.x + 10, rect.y + 68 + j * 14))

            # Barre de niveaux (petits carrés)
            for k in range(t["max"]):
                cx = rect.x + 10 + k * 18
                cy = rect.y + rect.height - 22
                coul = (255, 220, 60) if k < t["niveau"] else (76, 57, 40)
                pygame.draw.rect(fenetre, coul, (cx, cy, 14, 10), border_radius=2)
                pygame.draw.rect(fenetre, (147, 113, 76), (cx, cy, 14, 10), width=1, border_radius=2)

            # Texte niv actuel
            niv_txt = f"Niv {t['niveau']}/{t['max']}"
            coul_niv = (255, 200, 50) if t["niveau"] > 0 else (120, 130, 150)
            if maximal:
                niv_txt = "MAX"
                coul_niv = (255, 180, 40)
            s_niv = self.police_niv.render(niv_txt, True, coul_niv)
            fenetre.blit(s_niv, (rect.right - s_niv.get_width() - 8, rect.bottom - 20))

