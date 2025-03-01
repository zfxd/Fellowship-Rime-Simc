"""Module for a base Character class."""
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .basespell import BaseSpell

class BaseCharacter:
    """Even baser class for all characters."""

    def __init__(self, main_stat, crit, expertise, haste, spirit):
        self.main_stat = main_stat

        # Take and store these as PERCENTAGES.
        # Calculate these values from base in the character-specific class
        # if necessary. Different classes might have different DRs.
        self.crit = crit
        self.expertise = expertise
        self.haste = haste
        self.spirit = spirit
        self.rotation: List[BaseSpell] = []
        self.talents: List[str] = []

    def add_spell_to_rotation(self, spell: "BaseSpell") -> None:
        """Adds a spell to the character's rotation."""
        self.rotation.append(spell.value)

    def add_talent(self, talent: str) -> None:
        """Adds a talent to the character."""
        self.talents.append(talent)
