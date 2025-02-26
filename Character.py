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
        self.talents = [] # All the talents.
        self.anima_spikes = Spell("Anima Spikes", cast_time=0, cooldown=0, mana_generation=0, winter_orb_cost=0, damage_percent=36, hits=3)
        #Damage is set to 1560 because of ingame bug.
        self.soulfrost = Spell("Soulfrost Torrent", cast_time=2.0, cooldown=10, mana_generation=12, winter_orb_cost=0, damage_percent=1560, channeled=True, ticks=12)
        self.boosted_blast = Spell("Glacial Blast", cast_time=0, cooldown=0, mana_generation=0, winter_orb_cost=2, damage_percent=604)

        self.soulfrost_buff = Spell("Soulfrost Torrent", isBuff=True, debuffDuration=100000)
        self.glacial_assault_buff = Spell("Glacial Assault", isBuff=True, debuffDuration=100000)
        self.cometBonus = Spell("Ice Comet", cast_time=0, cooldown=0, mana_generation=0, winter_orb_cost=0, damage_percent=300)

    def add_spell(self, spell):
        self.spells.append(spell)
    
    def add_talent(self, talent):
        self.talents.append(talent)

    def update_stats(self, intellect, crit, expertise, haste, spirit):
        self.intellect = intellect * Character.intellectPerPoint
        self.crit = crit * Character.critPerPoint
        self.expertise = expertise * Character.expertisePerPoint
        self.haste = haste * Character.hastePerPoint
        self.spirit = spirit * Character.spiritPerPoint