import random
from Spell import Spell
from copy import copy

class Simulation:
    def __init__(self, character, duration, doDebug = True):
        self.character = character
        self.time = 0
        self.duration = duration
        self.total_damage = 0
        self.doDebug = doDebug
        self.gcd = 0
        self.debuffs = []
        self.buffs = []

    def gain_orb(self, doSpikes = True):
        self.character.winter_orbs += 1
        if doSpikes:
            for i in range(self.character.anima_spikes.hits):
                damage = self.character.anima_spikes.damage(self.character)
                self.total_damage += damage
                if self.doDebug: print(f'Time {self.time:.2f}: Cast {self.character.anima_spikes.name}, dealing {damage:.2f} damage')

        if self.character.winter_orbs > 5:
            print("Over capped on Orbs")
            self.character.winter_orbs = 5

    def do_damage(self, spell, damage, anima_gained, orb_cost, isCast = True):
        for buff in self.buffs[:]:
            if buff.name == "Wrath of Winter":
                damage *= 1.15
                
        self.total_damage += damage
        self.character.mana += anima_gained
        if orb_cost < 0:
            self.gain_orb()
        else:
            self.character.winter_orbs -= orb_cost

        if self.character.mana >= 10:
            self.character.mana = 0
            self.gain_orb()
        if self.doDebug: 
            if isCast: print(f'Time {self.time:.2f}: Cast {spell.name}, dealing {damage:.2f} damage')
            else: print(f'Time {self.time:.2f}: {spell.name} Ticks for {damage:.2f} damage')
        if orb_cost > 0 and random.uniform(0, 100) < self.character.spirit:
            self.gain_orb()

        if spell.name == "Cold Snap":
            for i in range (10):
                self.do_dance_of_swallows()
        if spell.name == "Freezing Torrent":
                self.do_dance_of_swallows()

    #Handle Swallows.
    def do_dance_of_swallows(self):
        for debuff in self.debuffs:
            if debuff.name == "Dance of Swallows":
                damage = debuff.damage(self.character)
                self.total_damage += damage
                if self.doDebug: print(f'Time {self.time:.2f}: Cast {debuff.name}, dealing {damage:.2f} damage')

    #Handle Upgrade Time
    def update_time(self, delta_time):
        self.time += delta_time
        self.gcd -= delta_time

        # Update spell cooldowns
        for spell in self.character.spells:
            spell.update_cooldown(delta_time)

        # Process debuffs
        for debuff in self.debuffs:  # Iterate over a copy to avoid modification issues
            debuff.update_remaining_debuff_duration(delta_time)
            # Handle multiple ticks within the delta_time interval
            if debuff.ticks > 0:
                while self.time >= debuff.next_tick_time:
                    self.do_damage(debuff, debuff.damage(self.character) / debuff.ticks, debuff.mana_generation / debuff.ticks, debuff.winter_orb_cost, False)
                    debuff.next_tick_time += debuff.debuffDuration / debuff.ticks  # Schedule next tick

            # Remove expired debuff
            if debuff.remaining_debuff_duration <= 0:
                if self.doDebug: print(f'Removing {debuff.name}')
                self.debuffs.remove(debuff)

        # Process buffs similarly
        for buff in self.buffs:
            buff.update_remaining_debuff_duration(delta_time)

            if buff.ticks > 0:
                while self.time >= buff.next_tick_time:
                    if buff.name == "Wrath of Winter":
                        self.gain_orb()
                buff.next_tick_time += buff.debuffDuration / buff.ticks  # Schedule next tick

            if buff.remaining_debuff_duration <= 0:
                self.buffs.remove(buff)

                #Hacky Buff Handling
                if buff.name == "Wrath of Winter":
                    self.character.haste -= 30

    #Generic Run
    def run(self):
        for spell in self.character.spells:
            spell.reset_cooldown()

        while self.time < self.duration:
            spell = None

            if self.gcd > 0:
                self.update_time(self.gcd)

            #Locate a spell that we can cast.
            for candidate_spell in self.character.spells:
                if candidate_spell.is_ready(self.character):
                    spell = candidate_spell
                    break
            
            if spell is None:
                if self.doDebug: print(f'Time {self.time:.2f}: No ready spell available')
                continue

            self.gcd = 1 / (1 + self.character.haste / 100)

            #Update the cooldown on the spell.
            spell.set_cooldown()

            if spell.channeled:
                for i in range(spell.ticks):
                    self.do_damage(spell, spell.damage(self.character) / spell.ticks, spell.mana_generation / spell.ticks, spell.winter_orb_cost)
                    self.update_time(spell.effective_cast_time(self.character) / spell.ticks)

            elif spell.isDebuff:
                self.update_time(spell.effective_cast_time(self.character))
                if self.doDebug: print(f'Time {self.time:.2f}: Cast {spell.name}.')
                spell.apply_debuff()
                if(spell.ticks > 0):
                    spell.next_tick_time = self.time + spell.debuffDuration / spell.ticks
                self.debuffs.append(spell)
            elif spell.isBuff:
                self.update_time(spell.effective_cast_time(self.character))
                if self.doDebug: print(f'Time {self.time:.2f}: Cast {spell.name}.')
                #Lazy coding
                spell.apply_debuff()
                if(spell.ticks > 0):
                    spell.next_tick_time = self.time + spell.debuffDuration / spell.ticks
                self.buffs.append(spell)

                #Hacky Buff Coding    
                if spell.name == "Wrath of Winter":
                    self.character.haste += 30
            else:
                self.update_time(spell.effective_cast_time(self.character))
                self.do_damage(spell, spell.damage(self.character), spell.mana_generation, spell.winter_orb_cost)

        dps = self.total_damage / self.duration
        if self.doDebug: print(f'Total Damage: {self.total_damage:.2f}, DPS: {dps:.2f}')
        return dps