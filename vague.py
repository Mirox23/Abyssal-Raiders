from mob import Mob, MobBoss, MobKamikaze, MobRapide, MobSoigneur, MobTank
from contenu_vagues.generateur_vagues import charger_configuration


CLASSES_MOBS = {
    "Mob": Mob,
    "MobRapide": MobRapide,
    "MobTank": MobTank,
    "MobKamikaze": MobKamikaze,
    "MobSoigneur": MobSoigneur,
}


class GestionnaireVague:
    def __init__(self):
        self.continent = "pirate"
        self.niveau = 1
        self.configuration_vagues = {}
        self.numero_vague = 0
        self.mobs_a_spawner = []
        self.vague_en_cours = False
        self.vague_terminee = False
        self.est_vague_boss = False
        self._spawn_position = (0, 0)
        self._temps_vague = 0.0

    def configurer_contexte(self, continent, niveau):
        self.continent = str(continent or "pirate").lower()
        self.niveau = max(1, int(niveau))
        self.configuration_vagues = charger_configuration(self.continent, self.niveau)
        self.numero_vague = 0
        self.mobs_a_spawner = []
        self.vague_en_cours = False
        self.vague_terminee = False
        self.est_vague_boss = False

    def demarrer_vague(self, spawn_position, est_boss=False):
        self._spawn_position = spawn_position
        self._temps_vague = 0.0
        self.vague_terminee = False
        self.vague_en_cours = True
        self.est_vague_boss = bool(est_boss)
        self.numero_vague += 1
        self.mobs_a_spawner = []

        if self.est_vague_boss:
            self.mobs_a_spawner.append((0.0, MobBoss, 0.0))
            return

        configuration = self.configuration_vagues.get(self.numero_vague, self.configuration_vagues.get(1, {}))
        intervalle = float(configuration.get("intervalle_spawn", 0.8))
        temps_courant = 0.0

        for groupe in configuration.get("groupes", []):
            type_mob = groupe.get("type", "Mob")
            classe_mob = CLASSES_MOBS.get(type_mob, Mob)
            nombre = max(1, int(groupe.get("nombre", 1)))
            decalage = float(groupe.get("decalage", 0.0))
            bonus_vitesse = float(groupe.get("bonus_vitesse", 0.0))
            for _ in range(nombre):
                self.mobs_a_spawner.append((temps_courant + decalage, classe_mob, bonus_vitesse))
                temps_courant += intervalle

    def mettre_a_jour(self, delta_temps, liste_ennemis, chemin):
        if not self.vague_en_cours:
            return

        self._temps_vague += delta_temps

        while self.mobs_a_spawner and self.mobs_a_spawner[0][0] <= self._temps_vague:
            _, classe_mob, bonus_vitesse = self.mobs_a_spawner.pop(0)
            vitesse = getattr(classe_mob, "vitesse_de_base", 100.0) * (1.0 + max(0.0, bonus_vitesse))
            liste_ennemis.append(classe_mob(self._spawn_position, vitesse=vitesse))

        if not self.mobs_a_spawner and not liste_ennemis:
            self.vague_en_cours = False
            self.vague_terminee = True
