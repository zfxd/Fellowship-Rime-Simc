import random
class Spell:
    def __init__(self, name, cast_time, cooldown, mana_generation, winter_orb_cost, damage_percent, hits=1, channeled = False, ticks = 0, isDebuff = False, debuffDuration = 0, doDebuffDamage = False, isBuff = False):
        self.name = name
        self.base_cast_time = cast_time
        self.cooldown = cooldown
        self.mana_generation = mana_generation
        self.winter_orb_cost = winter_orb_cost
        self.damage_percent = damage_percent / 100  # Convert to multiplier
        self.hits = hits  # Number of hits per cast
        self.remaining_cooldown = 0  # Tracks cooldown time remaining
        self.channeled = channeled
        self.isDebuff = isDebuff
        self.debuffDuration = debuffDuration
        self.remaining_debuff_duration = 0
        self.ticks = ticks
        self.next_tick_time = 0
        self.doDebuffDamage = doDebuffDamage
        self.isBuff = isBuff
        self.totalDamageDealt = 0

    def effective_cast_time(self, character):
        return self.base_cast_time * (1 - character.haste / 100)

    def is_ready(self, character):
        if self.winter_orb_cost <= character.winter_orbs:
            if self.remaining_cooldown <= 0:
                return True
        return False
    
    def damage(self, character):
        base_damage = self.damage_percent * character.intellect
        modified_damage = base_damage * (1 + character.expertise / 100)
        if random.uniform(0, 100) < character.crit:
            modified_damage *= 2  # Critical hit
        return modified_damage

    def set_cooldown(self):
        self.remaining_cooldown = self.cooldown

    def reset_cooldown(self):
        self.totalDamageDealt = 0
        self.remaining_cooldown = 0

    def update_cooldown(self, delta_time):
        # Decrease remaining cooldown by the delta time
        if self.remaining_cooldown > 0:
            self.remaining_cooldown -= delta_time

    def apply_debuff(self):
        # print(f'Applying {self.name}')
        self.remaining_debuff_duration = self.debuffDuration
        self.next_tick_time = 0
    
    def update_remaining_debuff_duration(self, delta_time):
        if self.remaining_debuff_duration > 0:
            self.remaining_debuff_duration -= delta_time