"""Main file for simulating Character DPS."""

import argparse
from copy import copy

from base import Character
from characters.Rime import RimeSpell
from Sim import Simulation


def main(args: argparse.Namespace):
    """Main function."""

    print("----------------------------")
    print("Starting new Sim")
    print("----------------------------")
    # Create your character below by
    # plugging in their Point Stats, not % Stats.
    # Test Character
    character = Character(
        intellect=300, crit=160, expertise=90, haste=120, spirit=50
    )

    # Talents
    # Row 1 - 2 Points Each
    # character.add_talent("Chillblain")
    character.add_talent("Coalescing Ice")
    # character.add_talent("Glacial Assault") #Doodoo
    # Row 2 - 1 Point Each
    character.add_talent("Unrelenting Ice")
    character.add_talent("Icy Flow")
    # Row 3 - 3 Points Each
    # character.add_talent("Wisdom of the North")
    # character.add_talent("Avalanche")
    character.add_talent("Soulfrost Torrent")

    # Spells casted in order.
    character.add_spell_to_rotation(RimeSpell.WRATH_OF_WINTER)
    character.add_spell_to_rotation(RimeSpell.ICE_BLITZ)
    character.add_spell_to_rotation(RimeSpell.DANCE_OF_SWALLOWS)
    # character.add_spell(RimeSpell.ICE_COMET)
    # character.add_spell(RimeSpell.GLACIAL_BLAST)
    character.add_spell_to_rotation(RimeSpell.COLD_SNAP)
    character.add_spell_to_rotation(RimeSpell.BURSTING_ICE)
    character.add_spell_to_rotation(RimeSpell.ICE_COMET)
    character.add_spell_to_rotation(RimeSpell.GLACIAL_BLAST)
    character.add_spell_to_rotation(RimeSpell.FREEZING_TORRENT)
    character.add_spell_to_rotation(RimeSpell.FROST_BOLT)

    # Sim Options - Uncomment one to run.
    match args.simulation_type:
        case "average_dps":
            average_dps(character, args.enemy_count)
        case "stat_weights":
            stat_weights(character)
        case "debug_sim":
            debug_sim(character)


def stat_weights(character: Character) -> None:
    """Calculates the stat weights of the character."""

    print("==== Doing Stat Weights ==== ")
    stat_increase = 200
    target_count = 4
    character_base = character
    base_dps = average_dps(character_base, target_count)

    character_updated = character
    character_updated.update_stats(
        intellect=character_updated.intellect_points + stat_increase,
        crit=character_updated.crit_points,
        expertise=character_updated.expertise_points,
        haste=character_updated.haste_points,
        spirit=character_updated.spirit_points,
    )
    int_dps = average_dps(character_updated, target_count)

    character_updated = character
    character_updated.update_stats(
        intellect=character_updated.intellect_points,
        crit=character_updated.crit_points + stat_increase,
        expertise=character_updated.expertise_points,
        haste=character_updated.haste_points,
        spirit=character_updated.spirit_points,
    )
    crit_dps = average_dps(character_updated, target_count)

    character_updated = character
    character_updated.update_stats(
        intellect=character_updated.intellect_points,
        crit=character_updated.crit_points,
        expertise=character_updated.expertise_points + stat_increase,
        haste=character_updated.haste_points,
        spirit=character_updated.spirit_points,
    )
    expertise_dps = average_dps(character_updated, target_count)

    character_updated = character
    character_updated.update_stats(
        intellect=character_updated.intellect_points,
        crit=character_updated.crit_points,
        expertise=character_updated.expertise_points,
        haste=character_updated.haste_points + stat_increase,
        spirit=character_updated.spirit_points,
    )
    haste_dps = average_dps(character_updated, target_count)

    character_updated = character
    character_updated.update_stats(
        intellect=character_updated.intellect_points,
        crit=character_updated.crit_points,
        expertise=character_updated.expertise_points,
        haste=character_updated.haste_points,
        spirit=character_updated.spirit_points + stat_increase,
    )
    spirit_dps = average_dps(character_updated, target_count)

    print("--------------")
    print("Stat Weights:")
    print(f"Intellect: {1 + ((int_dps - base_dps) / base_dps):.2f}")
    print(f"Crit: {1 + ((crit_dps - base_dps) / base_dps):.2f}")
    print(f"Expertise: {1 + ((expertise_dps - base_dps) / base_dps):.2f}")
    print(f"Haste: {1 + ((haste_dps - base_dps) / base_dps):.2f}")
    print(f"Spirit: {1 + ((spirit_dps - base_dps) / base_dps):.2f}")
    print("--------------")


def debug_sim(character: Character) -> None:
    """Runs a debug simulation."""

    sim = Simulation(character, duration=120, do_debug=True)
    sim.run()


def average_dps(character: Character, enemy_count: int) -> float:
    """Runs a simulation and returns the average DPS."""

    run_count = 2000
    dps_running_total = 0
    dps_lowest = 1000000
    dps_highest = 0
    for _ in range(run_count):
        character_copy = copy(character)
        sim = Simulation(
            character_copy,
            duration=180,
            enemy_count=enemy_count,
            do_debug=False,
        )
        dps = sim.run()
        dps_lowest = min(dps, dps_lowest)
        dps_highest = max(dps, dps_highest)

        dps_running_total += dps
    avg_dps = dps_running_total / run_count
    print(f"Highest DPS: {dps_highest:.2f}")
    print(f"Average DPS: {avg_dps:.2f}")
    print(f"Lowest DPS: {dps_lowest:.2f}")

    return avg_dps


if __name__ == "__main__":
    # Create parser for command line arguments.
    parser = argparse.ArgumentParser(description="Simulate Rime DPS.")

    parser.add_argument(
        "-s",
        "--simulation-type",
        type=str,
        default="average_dps",
        help="Type of simulation to run.",
        choices=["average_dps", "stat_weights", "debug_sim"],
        required=True,
    )
    parser.add_argument(
        "-e",
        "--enemy-count",
        type=int,
        default=1,
        help="Number of enemies to simulate.",
    )

    # Parse arguments.
    args = parser.parse_args()

    # Run the simulation.
    main(args)
