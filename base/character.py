"""Module for the Character class."""

from typing import List

from characters.Rime import RimeSpell

from .spell import Spell


class Character:
    """Base class for all characters."""

    intellectPerPoint = 1
    critPerPoint = 0.21
    expertisePerPoint = 0.21
    hastePerPoint = 0.21
    spiritPerPoint = 0.21

    def __init__(self, intellect, crit, expertise, haste, spirit):
        self.intellect_points = intellect
        self.intellect = intellect * Character.intellectPerPoint
        self.crit_points = crit
        self.crit = (  # % chance (e.g., 5 for 5%)
            crit * Character.critPerPoint
        ) + 5
        self.expertise_points = expertise
        self.expertise = (  # % increase to damage
            expertise * Character.expertisePerPoint
        )
        self.haste_points = haste
        # % increase to cast speed
        self.haste = haste * Character.hastePerPoint
        self.spirit = spirit * Character.spiritPerPoint
        self.spirit_points = spirit
        self.mana = 0
        self.winter_orbs = 0
        # This will hold the character's available spells.
        self.spells: List[Spell] = [spell.value for spell in RimeSpell]
        # This will hold the character's rotation.
        self.rotation: List[Spell] = []
        # All the talents.
        self.talents: List[str] = []
        self.anima_spikes = Spell(
            "Anima Spikes",
            cast_time=0,
            cooldown=0,
            mana_generation=0,
            winter_orb_cost=0,
            damage_percent=36,
            hits=3,
        )
        # Damage is set to 1560 because of ingame bug.
        self.soulfrost = Spell(
            "Soulfrost Torrent",
            cast_time=2.0,
            cooldown=10,
            mana_generation=12,
            winter_orb_cost=0,
            damage_percent=1560,
            channeled=True,
            ticks=12,
        )
        self.boosted_blast = Spell(
            "Glacial Blast",
            cast_time=0,
            cooldown=0,
            mana_generation=0,
            winter_orb_cost=2,
            damage_percent=604,
        )

        self.soulfrost_buff = Spell(
            "Soulfrost Torrent", is_buff=True, debuff_duration=100000
        )
        self.glacial_assault_buff = Spell(
            "Glacial Assault", is_buff=True, debuff_duration=100000
        )
        self.comet_bonus = Spell(
            "Ice Comet",
            cast_time=0,
            cooldown=0,
            mana_generation=0,
            winter_orb_cost=0,
            damage_percent=300,
        )

    def add_spell_to_rotation(self, spell: RimeSpell) -> None:
        """Adds a spell to the character's rotation."""

        if spell.value not in self.spells:
            raise ValueError(f"Spell {spell} not found in available spells.")

        self.rotation.append(spell.value)

    def add_talent(self, talent: str) -> None:
        """Adds a talent to the character's available talents."""

        self.talents.append(talent)

    def update_stats(
        self,
        intellect: int,
        crit: int,
        expertise: int,
        haste: int,
        spirit: int,
    ) -> None:
        """Updates the character's stats."""

        self.intellect = intellect * Character.intellectPerPoint
        self.crit = crit * Character.critPerPoint
        self.expertise = expertise * Character.expertisePerPoint
        self.haste = haste * Character.hastePerPoint
        self.spirit = spirit * Character.spiritPerPoint
