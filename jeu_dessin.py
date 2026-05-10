"""
Qu'est-ce que le fichier gère : Ce fichier gère le dessin du jeu.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Résultat : Des comportements, calculs ou affichages utilisés par le jeu.
"""

import os
import pygame
import math as _math

class JeuDessin:
    """
    Classe qui gère le dessin du jeu.
    Séparée de la classe principale Jeu pour respecter la limite de 300 lignes.
    """
    
    def __init__(self, jeu_instance):
        """
        Explication de ce que fais la fonction : Cette fonction initialise le système de dessin.
        Les entrées : jeu_instance.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        self.jeu = jeu_instance
        
    def dessiner(self):
        """
        Explication de ce que fais la fonction : Cette fonction dessine tous les éléments du jeu.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Affiche le jeu à l'écran.
        """
        fenetre_reelle = self.jeu.fenetre
        self.jeu.fenetre = self.jeu.surface_logique

        # Screen shake : décaler toute la surface de rendu 
        ox, oy = self.jeu._shake_offset

        # Fond : image du continent si dispo, sinon couleur unie de secours
        if self.jeu.image_fond:
            self.jeu.fenetre.blit(self.jeu.image_fond, (0, 0))
        else:
            self.jeu.fenetre.fill((32, 35, 55) if self.jeu.mode_fete else couleur_fond)
        draw_decor(self.jeu.fenetre, pygame)
        draw_path(self.jeu.fenetre, pygame)

        # Dessiner l'indicateur de direction des mobs (50 pixels pour être bien visible)
        self._dessiner_indicateur_direction(ox, oy)

        # Alarme visuelle : flash rouge sur le bord droit quand ennemi proche du mur 
        self._dessiner_alarme_murs(ox, oy)

        # Dessiner les tours et ennemis
        for tour in self.jeu.liste_tours:
            tour.dessiner(self.jeu.fenetre)
        for ennemi in self.jeu.liste_ennemis:
            ennemi.dessiner(self.jeu.fenetre)

        # HUD principal (avec shake)
        self._dessiner_hud(ox, oy)

        # Dessiner les effets visuels
        self._dessiner_effets_visuels()

        # Dessiner les éléments d'interface
        self._dessiner_interface()

        # Redimensionnement final
        pygame.transform.scale(self.jeu.surface_logique, (largeur_ecran, hauteur_ecran), fenetre_reelle)
        pygame.display.flip()
    
    def _dessiner_indicateur_direction(self, ox, oy):
        """
        Explication de ce que fais la fonction : Cette fonction dessine l'indicateur de direction.
        Les entrées : ox, oy.
        Le résultat : Affiche la flèche directionnelle.
        """
        if self.jeu._indicateur_direction_actif:
            pos_x, pos_y = self.jeu._position_indicateur
            dir_x, dir_y = self.jeu._direction_indicateur
            
            # Point de départ de la flèche
            depart_x = pos_x + ox
            depart_y = pos_y + oy
            
            # Agrandir la direction pour une flèche de 50 pixels
            facteur_agrandissement = 5  # 5 fois plus grande que 10 pixels
            arrivee_x = depart_x + dir_x * facteur_agrandissement
            arrivee_y = depart_y + dir_y * facteur_agrandissement
            
            # Dessiner la ligne principale plus épaisse
            pygame.draw.line(self.jeu.fenetre, (255, 50, 50), 
                           (depart_x, depart_y), (arrivee_x, arrivee_y), 8)
            
            # Dessiner une bordure blanche pour encore plus de visibilité
            pygame.draw.line(self.jeu.fenetre, (255, 255, 255), 
                           (depart_x, depart_y), (arrivee_x, arrivee_y), 10)
            pygame.draw.line(self.jeu.fenetre, (255, 50, 50), 
                           (depart_x, depart_y), (arrivee_x, arrivee_y), 6)
            
            # Dessiner une grande flèche au bout
            angle = _math.atan2(dir_y, dir_x)
            taille_pointe = 15  # Pointe beaucoup plus grande
            
            # Pointes latérales de la flèche
            pointe1_x = arrivee_x - taille_pointe * _math.cos(angle - 0.5)
            pointe1_y = arrivee_y - taille_pointe * _math.sin(angle - 0.5)
            pointe2_x = arrivee_x - taille_pointe * _math.cos(angle + 0.5)
            pointe2_y = arrivee_y - taille_pointe * _math.sin(angle + 0.5)
            
            # Dessiner la pointe avec bordure blanche
            pygame.draw.polygon(self.jeu.fenetre, (255, 255, 255),
                              [(arrivee_x, arrivee_y), (pointe1_x, pointe1_y), (pointe2_x, pointe2_y)])
            pygame.draw.polygon(self.jeu.fenetre, (255, 50, 50),
                              [(arrivee_x, arrivee_y), (pointe1_x-2, pointe1_y-2), (pointe2_x-2, pointe2_y-2)])
    
    def _dessiner_alarme_murs(self, ox, oy):
        """
        Explication de ce que fais la fonction : Cette fonction dessine l'alarme des murs.
        Les entrées : ox, oy.
        Le résultat : Affiche l'alarme visuelle.
        """
        mobs_danger = []
        for ennemi in self.jeu.liste_ennemis:
            if ennemi.x >= position_mur - 200:
                mobs_danger.append(ennemi)
        if mobs_danger:
            alpha = int(55 + 45 * _math.sin(self.jeu._alarme_clignotement * 7))
            alpha = max(0, min(140, alpha))
            surf_alarme = pygame.Surface((220, hauteur_ecran), pygame.SRCALPHA)
            surf_alarme.fill((255, 40, 40, alpha))
            self.jeu.fenetre.blit(surf_alarme, (position_mur - 200 + ox, oy))
    
    def _dessiner_hud(self, ox, oy):
        """
        Explication de ce que fais la fonction : Cette fonction dessine le HUD.
        Les entrées : ox, oy.
        Le résultat : Affiche l'interface utilisateur.
        """
        couleur_texte = (220, 220, 240)
        
        # HUD principal (avec shake)
        self.jeu.fenetre.blit(self.jeu.police_hud.render(f"Vie : {self.jeu.points_de_vie_mur}", True, couleur_texte), (20 + ox, 20 + oy))
        
        # Charger et afficher l'image de la pièce à côté de l'argent
        image_piece = None
        for chemin_piece in ["image/coin.png"]:
            if os.path.exists(chemin_piece):
                try:
                    image_piece = pygame.image.load(chemin_piece).convert_alpha()
                    # Redimensionner à la taille de la police
                    taille_police = self.jeu.police_hud.size("¤")
                    image_piece = pygame.transform.scale(image_piece, (taille_police[1], taille_police[1]))
                    break
                except Exception:
                    pass
        
        # Afficher le texte de l'argent
        texte_argent = self.jeu.police_hud.render(f"Argent : {self.jeu.argent}", True, couleur_texte)
        pos_argent = (20 + ox, 48 + oy)
        self.jeu.fenetre.blit(texte_argent, pos_argent)
        
        # Afficher l'image de la pièce si chargée
        if image_piece:
            pos_piece = (pos_argent[0] + texte_argent.get_width() + 8, pos_argent[1])
            self.jeu.fenetre.blit(image_piece, pos_piece)
        
        # Afficher le symbole ¤ après la pièce
        symbole = self.jeu.police_hud.render("¤", True, couleur_texte)
        pos_symbole = (pos_argent[0] + texte_argent.get_width() + 40, pos_argent[1]) if image_piece else (pos_argent[0] + texte_argent.get_width() + 8, pos_argent[1])
        self.jeu.fenetre.blit(symbole, pos_symbole)

        # Compteur de mobs restants
        total_restants = len(self.jeu.liste_ennemis) + len(self.jeu.gestionnaire_vague.mobs_a_spawner)
        if self.jeu.gestionnaire_vague.vague_en_cours:
            surf_mobs = pygame.font.SysFont("consolas", 14).render(f"{total_restants} ennemi(s) restant(s)", True, (200, 180, 140))
            self.jeu.fenetre.blit(surf_mobs, (20 + ox, 74 + oy))

        # Titre vague
        if self.jeu.gestionnaire_vague.est_vague_boss and self.jeu.gestionnaire_vague.vague_en_cours:
            texte_vague = f"⚔ VAGUE BOSS {self.jeu.vague_locale}/{self.jeu.vague_max} ⚔"
            surf_vague = self.jeu.police_vague.render(texte_vague, True, (255, 80, 80))
            self.jeu.fenetre.blit(surf_vague, (largeur_ecran // 2 - surf_vague.get_width() // 2, 90 + oy))
        elif self.jeu.gestionnaire_vague.vague_en_cours:
            texte_vague = f"Vague {self.jeu.vague_locale}/{self.jeu.vague_max}"
            surf_vague = self.jeu.police_vague.render(texte_vague, True, (200, 200, 240))
            self.jeu.fenetre.blit(surf_vague, (largeur_ecran // 2 - surf_vague.get_width() // 2, 90 + oy))

        # Message bonus fidélité 
        if self.jeu._timer_message_fidelite > 0:
            alpha_fid = min(255, int(self.jeu._timer_message_fidelite * 80))
            surf_fid = pygame.font.SysFont("consolas", 16, bold=True).render(self.jeu._message_fidelite, True, (255, 220, 80))
            surf_fid.set_alpha(alpha_fid)
            self.jeu.fenetre.blit(surf_fid, (largeur_ecran // 2 - surf_fid.get_width() // 2, 50))

        # Message de victoire finale
        if self.jeu._timer_message_victoire > 0:
            self._dessiner_message_victoire()
    
    def _dessiner_message_victoire(self):
        """
        Explication de ce que fais la fonction : Cette fonction dessine le message de victoire.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Affiche le message de victoire avec effets.
        """
        police_victoire = pygame.font.SysFont("consolas", 48, bold=True)
        alpha_victoire = min(255, int(self.jeu._timer_message_victoire * 60))
        surf_victoire = police_victoire.render(self.jeu._message_victoire, True, (255, 215, 0))
        surf_victoire.set_alpha(alpha_victoire)
        
        # Effet de pulsation
        pulsation = _math.sin(self.jeu._timer_message_victoire * 8) * 5
        pos_x = self.jeu._position_message_victoire[0] - surf_victoire.get_width() // 2 + pulsation
        pos_y = self.jeu._position_message_victoire[1] - surf_victoire.get_height() // 2
        
        # Ombre du texte
        surf_ombre = police_victoire.render(self.jeu._message_victoire, True, (100, 50, 0))
        surf_ombre.set_alpha(alpha_victoire // 2)
        self.jeu.fenetre.blit(surf_ombre, (pos_x + 3, pos_y + 3))
        
        # Texte principal
        self.jeu.fenetre.blit(surf_victoire, (pos_x, pos_y))
    
    def _dessiner_effets_visuels(self):
        """
        Explication de ce que fais la fonction : Cette fonction dessine les effets visuels.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Affiche les effets spéciaux.
        """
        for effet in self.jeu.effets_visuels:
            ratio = effet["temps"] / effet["duree"]
            rayon = max(2, int(effet["rayon"] * (1 - ratio * 0.5)))
            pygame.draw.circle(self.jeu.fenetre, effet["couleur"], (int(effet["x"]), int(effet["y"])), rayon, max(1, int(3 * ratio)))
    
    def _dessiner_interface(self):
        """
        Explication de ce que fais la fonction : Cette fonction dessine l'interface.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Affiche les éléments d'interface.
        """
        if self.jeu.tour_actuellement_selectionnee:
            self.jeu._dessiner_info_tour()
        if self.jeu.mode_placement_actif and self.jeu.type_tour_a_placer is None:
            self.jeu._dessiner_menu_type_tour()
        self.jeu.telephone.dessiner(self.jeu.fenetre)
        self.jeu.panneau_infos.dessiner(self.jeu.fenetre)
        self.jeu.panneau_achevement.dessiner(self.jeu.fenetre)
        self.jeu.ecran_fin_vague.dessiner(self.jeu.fenetre)
        # marché et scores 
        self.jeu.fenetre_marche.dessiner(self.jeu.fenetre)
        self.jeu.fenetre_scores.dessiner(self.jeu.fenetre)
        self.jeu.panneau_competences.dessiner(self.jeu.fenetre)
        self.jeu.panneau_objets.dessiner(self.jeu.fenetre)
        self.jeu.fenetre_recompenses_talents.dessiner(self.jeu.fenetre)
        self.jeu.fenetre_niveau_conquis.dessiner(self.jeu.fenetre)
        self.jeu._dessiner_bouton_recompense()
        
        # Tutoriel
        if self.jeu.tutoriel:
            self.jeu.tutoriel.dessiner(self.jeu.fenetre)
