import random
from Spell import Spell
from copy import copy

class Simulation:
    def __init__(self, character, duration, enemyCount = 1, doDebug = True):
        self.character = character
        self.time = 0
        self.duration = duration
        self.total_damage = 0
        self.doDebug = doDebug
        self.gcd = 0
        self.debuffs = []
        self.buffs = []
        self.enemyCount = enemyCount

    # Whenever we gain orbs, we want to cast 3 Anime Spikes.
    def gain_orb(self, doSpikes = True):
        self.character.winter_orbs += 1
        if self.doDebug: print(f"Time {self.time:.2f}: Gained Orbs - Count: {self.character.winter_orbs}")
        self.update_time(0.01)
        if doSpikes:
            for i in range(self.character.anima_spikes.hits):
                damage = self.character.anima_spikes.damage(self.character)
                self.total_damage += damage
                if self.doDebug: print(f'Time {self.time:.2f}: Cast {self.character.anima_spikes.name}, dealing {damage:.2f} damage')

        # If we are capped on Orbs, cap on 5.
        if self.character.winter_orbs > 5:
            print("Over capped on Orbs")
            self.character.winter_orbs = 5

    def lose_orb(self, orb_cost):
        for i in range(orb_cost):
            self.character.winter_orbs -= 1
            if "Wisdom of the North" in self.character.talents:
                for spell in self.character.spells:
                    if spell.name == "Ice Blitz" or spell.name == "Dance of Swallows" or spell.name == "Winters Blessing":
                        spell.update_cooldown(1) ## Reduces the cooldown by 1.
        if orb_cost > 0 and self.doDebug: print(f"Time {self.time:.2f}: Used Orbs - Count: {self.character.winter_orbs}")
        if orb_cost > 0 and random.uniform(0, 100) < self.character.spirit:
            for i in range(orb_cost):
                self.gain_orb()

    # Handle all Damage.
    def do_damage(self, spell, damage, anima_gained, orb_cost, isCast = True):
        for buff in self.buffs[:]:
            # If we have Wrath of Winter active. Deal 15% more damage.
            if buff.name == "Wrath of Winter":
                damage *= 1.15
            if buff.name == "Ice Blitz":
                if "Wisdom of the North" in self.character.talents:
                    damage *= 1.25
                else:
                    damage *= 1.15

        if (spell.name == "Soulfrost Torrent" or spell.name == "Freezing Torrent") and "Chillblain" in self.character.talents:
            damage *= 1.2
        
        if spell.name == "Bursting Ice" and "Coalescing Ice" in self.character.talents:
            damage *= 1.2

        if "Avalanche" in self.character.talents and spell.name == "Ice Comet":
            if random.uniform(0, 100) < 30:
                if random.uniform(0, 100) < 8:
                    damage *= 3
                else:
                    damage *= 2

        if spell.name == "Cold Snap" and "Glacial Assault" in self.character.talents:
            self.character.glacial_assault_buff.apply_debuff()
            self.buffs.append(self.character.glacial_assault_buff)

        if (spell.name == "Soulfrost Torrent" or spell.name == "Freezing Torrent") and "Unrelenting Ice" in self.character.talents:
            for spell in self.character.spells:
                if spell.name == "Bursting Ice":
                    spell.update_cooldown(0.5)

        if "Icy Flow" in self.character.talents and (spell.name == "Anima Spikes" or spell.name == "Dance of Swallows"):
            for spell in self.character.spells:
                if spell.name == "Freezing Torrent":
                    spell.update_cooldown(0.2)

        aoeCount = 1
        if spell.name == "Ice Comet":
            aoeCount = self.enemyCount
        if (spell.name == "Soulfrost Torrent" or spell.name == "Freezing Torrent") and "Chillblain" in self.character.talents:
            aoeCount = min(self.enemyCount, 5)
        if (spell.name == "Bursting Ice"):
            aoeCount = self.enemyCount

        for i in range(aoeCount):
            # Crit Calcs
            critChance = self.character.crit

            # Check if Soulfrost Torrent to modify Anima Spikes.
            if "Soulfrost Torrent" in self.character.talents and (spell.name == "Anima Spikes" or spell.name == "Dance of Swallows"):
                critChance += 10
            if spell.name == "Glacial Blast" and "Glacial Assault" in self.character.talents:
                critChance += 20

            # Roll the Crit.    
            if random.uniform(0, 100) < critChance:
                damage *= 2  # Critical hit
                # Roll for Soulfrost Torrent buff.
                canApply = True
                if "Soulfrost Torrent" in self.character.talents and random.uniform(0,100) < 25:
                    for buff in self.buffs:
                        if buff.name == "Soulfrost Torrent": canApply = False
                    if canApply:
                        self.character.soulfrost_buff.apply_debuff()
                        self.buffs.append(self.character.soulfrost_buff)

            #Do other stuff.
            if (spell.name == "Soulfrost Torrent" or spell.name == "Freezing Torrent") and "Chillblain" in self.character.talents and i != 0:
                damage = damage * 0.2
            self.total_damage += damage

        if spell.name == "Bursting Ice" and "Coalescing Ice" in self.character.talents and self.enemyCount == 1:
            self.character.mana += 2
        self.character.mana += anima_gained
        for buff in self.buffs[:]:
            if buff.name == "Ice Blitz":
                for i in range(int(anima_gained)):
                    damage = self.character.anima_spikes.damage(self.character)
                    self.total_damage += damage
                    if self.doDebug: print(f'Time {self.time:.2f}: Cast {self.character.anima_spikes.name}, dealing {damage:.2f} damage')

        if self.doDebug: 
            if isCast: print(f'Time {self.time:.2f}: Your {spell.name} hit for {damage:.2f} damage')
            else: print(f'Time {self.time:.2f}: Your {spell.name} ticks for {damage:.2f} damage')
        
        if orb_cost < 0:
            self.gain_orb()
        else:
            self.lose_orb(orb_cost)

        if self.character.mana >= 10:
            self.character.mana = 0
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
                self.do_damage(debuff, debuff.damage(self.character), 0, 0)

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
                while self.time >= debuff.next_tick_time and debuff.remaining_debuff_duration > 0:
                    self.do_damage(debuff, debuff.damage(self.character) / debuff.ticks, debuff.mana_generation / debuff.ticks, debuff.winter_orb_cost, False)
                    debuff.next_tick_time += debuff.debuffDuration / debuff.ticks  # Schedule next tick

            # Remove expired debuff
            if debuff.remaining_debuff_duration <= 0:
                if debuff in self.debuffs:
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
                if candidate_spell.is_ready(self.character, self.enemyCount):
                    spell = candidate_spell
                    break
            
            if spell is None:
                if self.doDebug: print(f'Time {self.time:.2f}: No ready spell available')
                continue

            self.gcd = 1 / (1 + self.character.haste / 100)

            #Update the cooldown on the spell.
            if self.doDebug: print(f'Time {self.time:.2f}: Cast {spell.name}.')
            spell.set_cooldown()

            #Check to see if replacing Freezing with Soulfrost Torrent
            if spell.name == "Freezing Torrent":
                for buff in self.buffs[:]:
                    if buff.name == "Soulfrost Torrent":
                        spell = self.character.soulfrost
                        self.buffs.remove(buff)

            #Check to see if replacing Blast with Better Blast
            glacialAssaultCount = 0
            if spell.name == "Glacial Blast" and "Glacial Assault" in self.character.talents:
                for buff in self.buffs:
                    if buff.name == "Glacial Assault":
                        glacialAssaultCount += 1
                if glacialAssaultCount == 5:
                    for buff in self.buffs[:]:
                        if buff.name == "Glacial Assault":
                            self.buffs.remove(buff)
                    spell = self.character.boosted_blast

            self.update_time(0.01)

            if spell.channeled:
                for i in range(spell.ticks):
                    self.do_damage(spell, spell.damage(self.character) / spell.ticks, spell.mana_generation / spell.ticks, spell.winter_orb_cost)
                    self.update_time(spell.effective_cast_time(self.character) / spell.ticks)

            elif spell.isDebuff:
                self.update_time(spell.effective_cast_time(self.character))
                spell.apply_debuff()
                if spell.winter_orb_cost > 0:
                    self.lose_orb(spell.winter_orb_cost)
                if(spell.ticks > 0):
                    spell.next_tick_time = self.time + spell.debuffDuration / spell.ticks
                self.debuffs.append(spell)
            elif spell.isBuff:
                self.update_time(spell.effective_cast_time(self.character))
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