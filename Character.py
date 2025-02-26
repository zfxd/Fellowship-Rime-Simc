from Spell import Spell

class Character:
    intellectPerPoint = 1
    critPerPoint = 0.21
    expertisePerPoint = 0.21
    hastePerPoint = 0.21
    spiritPerPoint = 0.21
    def __init__(self, intellect, crit, expertise, haste, spirit):
        self.intellectPoints = intellect
        self.intellect = intellect * Character.intellectPerPoint
        self.critPoints = crit
        self.crit = (crit * Character.critPerPoint) + 5  # % chance (e.g., 5 for 5%)
        self.expertisePoints = expertise
        self.expertise = expertise * Character.expertisePerPoint  # % increase to damage
        self.hastePoints = haste
        self.haste = haste * Character.hastePerPoint  # % increase to cast speed
        self.spirit = spirit * Character.spiritPerPoint
        self.spiritPoints = spirit
        self.mana = 0
        self.winter_orbs = 0
        self.spells = []  # This will hold the character's available spells
        self.anima_spikes = Spell("Anima Spikes", cast_time=0, cooldown=0, mana_generation=0, winter_orb_cost=0, damage_percent=36, hits=3)

    def add_spell(self, spell):
        self.spells.append(spell)

    def update_stats(self, intellect, crit, expertise, haste, spirit):
        self.intellect = intellect * Character.intellectPerPoint
        self.crit = crit * Character.critPerPoint
        self.expertise = expertise * Character.expertisePerPoint
        self.haste = haste * Character.hastePerPoint
        self.spirit = spirit * Character.spiritPerPoint