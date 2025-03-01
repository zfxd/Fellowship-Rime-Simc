""" Launch this instead to simulate Tariq DPS """

import argparse
from typing import Optional
from copy import deepcopy

from base import BaseCharacter

def main(arguments: argparse.Namespace):
    """Main Function."""

    print("------------------")
    print("Starting facebreaker.py")
    print("------------------")

    
    # TODO Error checking here

    # TODO initialize character
    character = BaseCharacter(271, 24.47, 20.98, 12.40, 21.94)

    # TODO talents and rotation should be in its own file

    # TODO sim options - maybe later. One function per each?
    print(f"Run {arguments.sims} simulations for {arguments.duration} seconds with {arguments.enemy_count} enemies.")

    if(arguments.log):
        print("Displaying combat logs.")
    print("------------------")
    match arguments.simulation_type:
        case "average_dps":
            # TODO run simulation
            print("Running average_dps simulation")

    # TODO sims go here

if __name__ == "__main__":
    # Create parser for command line arguments.
    parser = argparse.ArgumentParser(description="Simulate Tariq DPS.")

    parser.add_argument(
        "-t",
        "--simulation-type",
        type=str,
        default="average_dps",
        help="Type of simulation to run.",
        choices=["average_dps"] # Maybe add more later
        #, required=True
    )
    parser.add_argument(
        "-d",
        "--duration",
        type=int,
        default=60,
        help="Duration of the simulation.",
    )

    parser.add_argument(
        "-e",
        "--enemy-count",
        type=int,
        default=1,
        help="Number of enemies to simulate.",
        required=True,
    )

    parser.add_argument(
        "-l",
        "--log",
        action="store_true",
        help="Display combat logs"
    )

    parser.add_argument(
        "-s",
        "--sims",
        type=int,
        default = 3,
        help="Number of simulations to run"
    )

    # Parse arguments.
    args = parser.parse_args()

    # Run the simulation
    main(args)