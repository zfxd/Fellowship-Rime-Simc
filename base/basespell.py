"""Module for the a base Spell class."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .character import BaseCharacter

class BaseSpell:
    """Even baser class for all spells."""

    def __init(
        self,
        name="",
        cast_time=0,
        cooldown=0,
        damage_percent=0,
        hits=1,
        channeled=False,
        ticks=0,
        is_debuff=False,
        debuff_duration=0,
        do_debuff_damage=False,
        is_buff=False,
        min_target_count=1,
        max_target_count=1000,
        ready=True
    ):
        self.name = name
        self.base_cast_time = cast_time
        self.cooldown = cooldown
        self.damage_percent = damage_percent / 100  # Convert to multiplier
        self.hits = hits                            # Number of hits per cast
        self.remaining_cooldown = 0                 # Tracks cooldown time remaining
        self.channeled = channeled
        self.is_debuff = is_debuff
        self.debuff_duration = debuff_duration
        self.remaining_debuff_duration = 0
        self.ticks = ticks
        self.next_tick_time = 0
        self.do_debuff_damage = do_debuff_damage
        self.is_buff = is_buff
        self.total_damage_dealt = 0                 # Might not be  needed
        self.min_target_count = min_target_count    # Minimum Needed Targets to cast this on.
        self.max_target_count = max_target_count    # Maximum Needed Targets to cast this on.
        self.ready = ready

    def effective_cast_time(self, character: "BaseCharacter") -> float:
        """Returns the effective cast time of the spell."""
        # Rime apparently works like this. But Tariq's cast times seem to be affected by haste weirdly.
        # Consider overwriting this method in the character-specific spells if the cast times are affected differently
        return self.base_cast_time * (1 - character.haste / 100)

    def is_ready(self, character: "BaseCharacter", enemy_count: int) -> bool:
        """Returns True if the spell is ready to be cast."""
        return self.ready
    
    def damage(self, character: "BaseCharacter") -> float:
        """Returns the damage of the spell."""
        base_damage = character.main_stat * self.damage_percent
        modified_damage = base_damage * (1 + character.expertise / 100)
        return modified_damage

    def set_cooldown(self, character: "BaseCharacter") -> None:
        """Sets the cooldown of the spell."""
        self.remaining_cooldown = self.cooldown

    def reset_cooldown(self) -> None:
        """Resets the cooldown of the spell."""
        self.remaining_cooldown = 0

    def update_cooldown(self, delta_time: int) -> None:
        """Decreases the remaining cooldown by the delta time."""
        if self.remaining_cooldown > 0:
            self.remaining_cooldown -= delta_time

    def apply_debuff(self) -> None:
        """Applies the debuff to the target."""

        self.remaining_debuff_duration = self.debuff_duration
        self.next_tick_time = 0

    def update_remaining_debuff_duration(self, delta_time: int) -> None:
        """Decreases the remaining debuff duration by the delta time."""

        if self.remaining_debuff_duration > 0:
            self.remaining_debuff_duration -= delta_time
