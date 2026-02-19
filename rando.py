from pathlib import Path
from dnd_character import Character
from dnd_character.classes import CLASSES, Wizard
from dnd_character.experience import experience_at_level
from dnd_character.equipment import Item
from dnd_character.spellcasting import SPELLS, spells_for_class_level, _SPELL
from dnd_character.dice import sum_rolls

from dnd_character.rich_ui import render


rando = Wizard(
    name="Rando B. Higgins",
    age="102",
    gender="Male",
    race="High Elf",
    species="Elf",
    alignment="CE",
    description="He wild",
    background="Don't ask",
    personality="Not really",
    ideals="Sure",
    bonds="No just stocks",
    flaws="Plenty",
    languages="Common",
    lore="Too long",
    level=1,
)
render(rando)
