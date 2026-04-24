class ProgressionMonde:
    def __init__(self):
        self.niveaux_conquis = {
            "pirate": [False] * 8,
            "medieval": [False] * 8,
            "samourai": [False] * 8,
            "demoniaque": [False] * 8,
        }

    def est_niveau_debloque(self, continent, numero_niveau):
        if numero_niveau <= 1:
            return True
        liste = self.niveaux_conquis.get(continent, [])
        if len(liste) < (numero_niveau - 1):
            return False
        return liste[numero_niveau - 2]

    def marquer_conquis(self, continent, numero_niveau):
        if continent not in self.niveaux_conquis:
            return
        if 1 <= numero_niveau <= 8:
            self.niveaux_conquis[continent][numero_niveau - 1] = True

    def est_conquis(self, continent, numero_niveau):
        if continent not in self.niveaux_conquis:
            return False
        if 1 <= numero_niveau <= 8:
            return self.niveaux_conquis[continent][numero_niveau - 1]
        return False

    def bonus_fidelite_argent(self, continent, numero_niveau):
        """
        NOUVEAU — Bonus de fidélité : +3 or de départ par niveau déjà conquis
        dans ce continent. Récompense les joueurs qui reviennent sur des niveaux maîtrisés.
        """
        if continent not in self.niveaux_conquis:
            return 0
        nb_conquis = sum(1 for c in self.niveaux_conquis[continent][:numero_niveau] if c)
        return nb_conquis * 3

    def bonus_fidelite_vie(self, continent, numero_niveau):
        """
        NOUVEAU — +1 PV de mur par tranche de 3 niveaux conquis dans le continent.
        """
        if continent not in self.niveaux_conquis:
            return 0
        nb_conquis = sum(1 for c in self.niveaux_conquis[continent][:numero_niveau] if c)
        return nb_conquis // 3