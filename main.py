from Character import Character
from Spell import Spell
from Sim import Simulation
from copy import copy

def main():
    print("----------------------------")
    print("Starting new Sim")
    print("----------------------------")
    # Create the character and add spells
    #My personal character
    #character = Character(intellect=157, crit=19, expertise=8, haste=36, spirit=29)
    #Top player ATM
    #character = Character(intellect=233, crit=26, expertise=64, haste=68, spirit=110)
    #Aari
    character = Character(intellect=179, crit=20, expertise=76, haste=29, spirit=22)
    #Kalle
    #character = Character(intellect=270, crit=60, expertise=140, haste=60, spirit=40)
    
    # Add spells to the character in priority order
    #character.add_spell(Spell("Wrath of Winter", cast_time=0, cooldown=600, mana_generation=0, winter_orb_cost=0, damage_percent=0, isBuff=True, ticks=10, debuffDuration=20))
    character.add_spell(Spell("Dance of Swallows", cast_time=0, cooldown=60, mana_generation=0, winter_orb_cost=2, damage_percent=53, isDebuff=True, ticks=0, debuffDuration=20))
    character.add_spell(Spell("Cold Snap", cast_time=0, cooldown=8, mana_generation=0, winter_orb_cost=-1, damage_percent=204))  # Cold Snap spell
    character.add_spell(Spell("Bursting Ice", cast_time=2.0, cooldown=10, mana_generation=6, winter_orb_cost=0, damage_percent=366, isDebuff=True, ticks=6, debuffDuration=3, doDebuffDamage=True))
    character.add_spell(Spell("Glacial Blast", cast_time=2.0, cooldown=0, mana_generation=0, winter_orb_cost=2, damage_percent=504))
    character.add_spell(Spell("Freezing Torrent", cast_time=2.0, cooldown=10, mana_generation=6, winter_orb_cost=0, damage_percent=390, channeled=True, ticks=6))
    character.add_spell(Spell("FrostBolt", cast_time=1.5, cooldown=0, mana_generation=3, winter_orb_cost=0, damage_percent=73))

    #Average DPS Calculation
    average_dps(character)
    #stat_weights(character)
    #debug_sim(character)


def stat_weights(character):
    print("==== Doing Stat Weights ==== ")
    statIncrease = 50
    characterBase = character
    baseDPS = average_dps(characterBase)

    characterUpdated = character
    characterUpdated.update_stats(intellect=characterUpdated.intellectPoints + statIncrease, crit=characterUpdated.critPoints, expertise=characterUpdated.expertisePoints, haste=characterUpdated.hastePoints, spirit=characterUpdated.spiritPoints)
    intDPS = average_dps(characterUpdated)

    characterUpdated = character
    characterUpdated.update_stats(intellect=characterUpdated.intellectPoints, crit=characterUpdated.critPoints + statIncrease, expertise=characterUpdated.expertisePoints, haste=characterUpdated.hastePoints, spirit=characterUpdated.spiritPoints)
    critDPS = average_dps(characterUpdated)

    characterUpdated = character
    characterUpdated.update_stats(intellect=characterUpdated.intellectPoints, crit=characterUpdated.critPoints, expertise=characterUpdated.expertisePoints + statIncrease, haste=characterUpdated.hastePoints, spirit=characterUpdated.spiritPoints)
    expertiseDPS = average_dps(characterUpdated)

    characterUpdated = character
    characterUpdated.update_stats(intellect=characterUpdated.intellectPoints, crit=characterUpdated.critPoints, expertise=characterUpdated.expertisePoints, haste=characterUpdated.hastePoints + statIncrease, spirit=characterUpdated.spiritPoints)
    hasteDPS = average_dps(characterUpdated)

    characterUpdated = character
    characterUpdated.update_stats(intellect=characterUpdated.intellectPoints, crit=characterUpdated.critPoints, expertise=characterUpdated.expertisePoints, haste=characterUpdated.hastePoints, spirit=characterUpdated.spiritPoints + statIncrease)
    spiritDPS = average_dps(characterUpdated)

    print(f'Stat Weights:')
    print(f'Intellect: {1 + ((intDPS - baseDPS) / baseDPS):.2f}')
    print(f'Crit: {1 + ((critDPS - baseDPS) / baseDPS):.2f}')
    print(f'Expertise: {1 + ((expertiseDPS - baseDPS) / baseDPS):.2f}')
    print(f'Haste: {1 + ((hasteDPS - baseDPS) / baseDPS):.2f}')
    print(f'Spirit: {1 + ((spiritDPS - baseDPS) / baseDPS):.2f}')
    print("--------------")

def debug_sim(character):
    sim = Simulation(character, duration=120, doDebug = True)
    sim.run()

def average_dps(character):
    runCount = 2000
    dpsRunningTotal = 0
    dpsLowest = 10000
    dpsHighest = 0
    for i in range(runCount):
        characterCopy = copy(character)
        sim = Simulation(characterCopy, duration=120, doDebug = False)
        dps = sim.run()
        if dps < dpsLowest:
            dpsLowest = dps
        if dps > dpsHighest:
            dpsHighest = dps
        dpsRunningTotal += dps
    averageDPS = dpsRunningTotal / runCount
    print(f'Highest DPS: {dpsHighest:.2f}')
    print(f'Average DPS: {averageDPS:.2f}')
    print(f'Lowest DPS: {dpsLowest:.2f}')
    return averageDPS

if __name__ == "__main__":
    main()