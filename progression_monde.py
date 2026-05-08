"""
Qu'est-ce que le fichier gère : Ce fichier gère la partie progression monde du projet.
Entrée : Les données nécessaires aux fonctions, classes et paramètres du module.
Résultat : Des comportements, calculs ou affichages utilisés par le jeu.
"""


class ProgressionMonde:
    def __init__(self):
        """
        Explication de ce que fais la fonction : Cette fonction exécute init.
        Les entrées : Cette fonction ne demande pas de paramètre direct.
        Le résultat : Initialise correctement les attributs de l'objet.
        """
        self.niveaux_conquis = {
            "pirate": [False] * 8,
            "medieval": [False] * 8,
            "samourai": [False] * 8,
            "demoniaque": [False] * 8,
        }
        self.succes_vagues = {
            cle: [[False] * 4 for _ in range(8)]
            for cle in self.niveaux_conquis
        }

    def est_niveau_debloque(self, continent, numero_niveau):
        """
        Explication de ce que fais la fonction : Cette fonction vérifie est niveau debloque.
        Les entrées : continent, numero_niveau.
        Le résultat : Retourne True ou False selon la condition vérifiée.
        """
        if numero_niveau <= 1:
            return True
        liste = self.niveaux_conquis.get(continent, [])
        if len(liste) < (numero_niveau - 1):
            return False
        return liste[numero_niveau - 2]

    def marquer_conquis(self, continent, numero_niveau):
        """
        Explication de ce que fais la fonction : Cette fonction exécute marquer conquis.
        Les entrées : continent, numero_niveau.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if continent not in self.niveaux_conquis:
            return
        if 1 <= numero_niveau <= 8:
            self.niveaux_conquis[continent][numero_niveau - 1] = True
            self.succes_vagues[continent][numero_niveau - 1] = [True, True, True, True]

    def est_conquis(self, continent, numero_niveau):
        """
        Explication de ce que fais la fonction : Cette fonction vérifie est conquis.
        Les entrées : continent, numero_niveau.
        Le résultat : Retourne True ou False selon la condition vérifiée.
        """
        if continent not in self.niveaux_conquis:
            return False
        if 1 <= numero_niveau <= 8:
            return self.niveaux_conquis[continent][numero_niveau - 1]
        return False

    def marquer_succes_vague(self, continent, numero_niveau, numero_vague):
        """
        Explication de ce que fais la fonction : Cette fonction exécute marquer succes vague.
        Les entrées : continent, numero_niveau, numero_vague.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if continent not in self.succes_vagues:
            return
        if not (1 <= numero_niveau <= 8 and 1 <= numero_vague <= 4):
            return
        succes = self.succes_vagues[continent][numero_niveau - 1]
        while len(succes) < 4:
            succes.append(False)
        self.succes_vagues[continent][numero_niveau - 1][numero_vague - 1] = True

    def succes_niveau(self, continent, numero_niveau):
        """
        Explication de ce que fais la fonction : Cette fonction exécute succes niveau.
        Les entrées : continent, numero_niveau.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if continent not in self.succes_vagues or not (1 <= numero_niveau <= 8):
            return [False, False, False, False]
        succes = list(self.succes_vagues[continent][numero_niveau - 1])
        while len(succes) < 4:
            succes.append(False)
        return succes[:4]

    def bonus_fidelite_argent(self, continent, numero_niveau):
        """
        Explication de ce que fais la fonction : Cette fonction exécute bonus fidelite argent.
        Les entrées : continent, numero_niveau.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if continent not in self.niveaux_conquis:
            return 0
        nb_conquis = sum(1 for c in self.niveaux_conquis[continent][:numero_niveau] if c)
        return nb_conquis * 3

    def bonus_fidelite_vie(self, continent, numero_niveau):
        """
        Explication de ce que fais la fonction : Cette fonction exécute bonus fidelite vie.
        Les entrées : continent, numero_niveau.
        Le résultat : Retourne la valeur attendue ou applique l'action prévue.
        """
        if continent not in self.niveaux_conquis:
            return 0
        nb_conquis = sum(1 for c in self.niveaux_conquis[continent][:numero_niveau] if c)
        return nb_conquis // 3
