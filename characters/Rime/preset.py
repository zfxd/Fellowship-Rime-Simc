"""Module for Rime's presets."""

from enum import Enum

from base import Character


class RimePreset(Enum):
    """Enum for Rime's presets."""

    DEFAULT = Character(
        intellect=300, crit=90, expertise=160, haste=120, spirit=50
    )
