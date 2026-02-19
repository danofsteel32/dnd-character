import functools
from dnd_character import Character
from dnd_character.classes import CLASSES, Wizard
from dnd_character.experience import experience_at_level
from dnd_character.equipment import Item
from dnd_character.spellcasting import SPELLS, spells_for_class_level, _SPELL
from dnd_character.dice import sum_rolls

from rich import box
from rich.columns import Columns
from rich.console import Console, RenderableType
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


class Emoji:
    wizard = "\U0001f9d9"


panel_common = functools.partial(
    Panel,
    expand=True,
    subtitle_align="left",
    border_style="bold",
    box=box.HEAVY,
)
right_aligned_text = functools.partial(
    Text,
    justify="right",
)


def get_header(c: Character, *, width: int) -> RenderableType:
    layout = Layout(name="header", size=6)

    name_section_width = int(width * 0.4)
    level_section_width = width - name_section_width
    level_column_width = int((level_section_width - 2) / 3)

    print(f"{name_section_width=} {level_section_width=} {level_column_width=}")

    layout.split_row(
        Layout(
            panel_common(f"{c.name}\n  {c.description}", subtitle="Name", padding=1),
            name="character_name",
            # ratio=4,
            size=name_section_width,
        ),
        Layout(
            Columns(
                [
                    panel_common(
                        right_aligned_text(f"{Emoji.wizard} {c.class_name} {c.level}"),
                        subtitle="Class & Level",
                    ),
                    panel_common(
                        right_aligned_text(c.background), subtitle="Background"
                    ),
                    panel_common(
                        right_aligned_text("INSERT_PLAYER_NAME"), subtitle="Player Name"
                    ),
                    panel_common(right_aligned_text(c.race), subtitle="Race"),
                    panel_common(right_aligned_text(c.alignment), subtitle="Alignment"),
                    panel_common(
                        right_aligned_text(str(c.experience)),
                        subtitle="Experience (XP)",
                    ),
                ],
                width=level_column_width,
            ),
            size=level_section_width,
        ),
    )
    return layout


def get_base_stats_column(c: Character) -> RenderableType:
    base_stat_panel = functools.partial(
        Panel,
        box=box.HEAVY,
        border_style="green",
    )
    base_stats_text = functools.partial(Text, justify="center", style="bold")

    base_stats_column = Layout(name="base_stats")
    base_stats_column.split_row(
        Columns(
            [
                base_stat_panel(
                    base_stats_text(
                        f"{c.strength}\n{c.get_ability_modifier(c.strength)}"
                    ),
                    subtitle="STR",
                ),
                base_stat_panel(
                    base_stats_text(
                        f"{c.dexterity}\n{c.get_ability_modifier(c.dexterity)}"
                    ),
                    subtitle="DEX",
                ),
                base_stat_panel(
                    base_stats_text(
                        f"{c.constitution}\n{c.get_ability_modifier(c.constitution)}"
                    ),
                    subtitle="CON",
                ),
                base_stat_panel(
                    base_stats_text(
                        f"{c.intelligence}\n{c.get_ability_modifier(c.intelligence)}"
                    ),
                    subtitle="INT",
                ),
                base_stat_panel(
                    base_stats_text(f"{c.wisdom}\n{c.get_ability_modifier(c.wisdom)}"),
                    subtitle="WIS",
                ),
                base_stat_panel(
                    base_stats_text(
                        f"{c.charisma}\n{c.get_ability_modifier(c.charisma)}"
                    ),
                    subtitle="CHA",
                ),
            ],
            width=9,
        )
    )
    return base_stats_column


glowing_white_text = functools.partial(Text, style="bold blink")
green_text = functools.partial(Text, style="bold green reverse")


def get_stats(c: Character, *, width: int) -> RenderableType:
    layout = Layout(ratio=6)

    insp_prof_table = Table.grid(expand=True)
    insp_prof_table.add_column(
        "BONUS",
    )
    insp_prof_table.add_column("STAT")
    insp_prof_table.add_row(str(c.inspiration), "Inspiration")
    insp_prof_table.add_row(str(c.prof_bonus), "Proficiency Bonus")
    insp_prof_table.add_row(
        str(10 + c.get_ability_modifier(c.wisdom)), "Passive Wisdom"
    )

    saving_throws_table = Table(box=box.SIMPLE, padding=(0, 0), expand=True)
    saving_throws_table.add_column("PROF")
    saving_throws_table.add_column("BNS")
    saving_throws_table.add_column("STAT")
    saving_throws_table.add_row("-", str(c.get_ability_modifier(c.strength)), "STR")
    saving_throws_table.add_row("-", str(c.get_ability_modifier(c.dexterity)), "DEX")
    saving_throws_table.add_row("-", str(c.get_ability_modifier(c.constitution)), "CON")
    saving_throws_table.add_row(
        green_text("+"),
        str(c.get_ability_modifier(c.intelligence) + c.prof_bonus),
        "INT",
    )
    saving_throws_table.add_row(
        green_text("+"), str(c.get_ability_modifier(c.wisdom) + c.prof_bonus), "WIS"
    )
    saving_throws_table.add_row("-", str(c.get_ability_modifier(c.charisma)), "CHA")

    skills_table = Table(box=box.SIMPLE, padding=(0, 0), expand=True)
    skills_table.add_column("PROF")
    skills_table.add_column("BNS")
    skills_table.add_column("SKILL")
    skills_table.add_column("STAT")
    skills_table.add_row(
        "-", str(c.get_ability_modifier(c.dexterity)), "Acrobatics", "DEX"
    )
    skills_table.add_row(
        "-", str(c.get_ability_modifier(c.wisdom)), "Animal Handling", "WIS"
    )
    skills_table.add_row(
        green_text("+"),
        str(c.get_ability_modifier(c.intelligence) + c.prof_bonus),
        "Arcana",
        "INT",
    )
    skills_table.add_row(
        "-", str(c.get_ability_modifier(c.strength)), "Athletics", "STR"
    )
    skills_table.add_row(
        "-", str(c.get_ability_modifier(c.charisma)), "Deception", "CHA"
    )
    skills_table.add_row(
        green_text("+"),
        str(c.get_ability_modifier(c.intelligence) + c.prof_bonus),
        "History",
        "INT",
    )
    skills_table.add_row("-", str(c.get_ability_modifier(c.wisdom)), "Insight", "WIS")
    skills_table.add_row(
        "-", str(c.get_ability_modifier(c.charisma)), "Intimidation", "CHA"
    )
    skills_table.add_row(
        "-", str(c.get_ability_modifier(c.intelligence)), "Investigation", "INT"
    )
    skills_table.add_row("-", str(c.get_ability_modifier(c.wisdom)), "Medicine", "WIS")
    skills_table.add_row(
        "-", str(c.get_ability_modifier(c.intelligence)), "Nature", "INT"
    )
    skills_table.add_row(
        "-", str(c.get_ability_modifier(c.wisdom)), "Perception", "WIS"
    )
    skills_table.add_row(
        "-", str(c.get_ability_modifier(c.charisma)), "Performance", "CHA"
    )
    skills_table.add_row(
        "-", str(c.get_ability_modifier(c.intelligence)), "Religion", "INT"
    )
    skills_table.add_row(
        "-", str(c.get_ability_modifier(c.dexterity)), "Sleight of Hand", "DEX"
    )
    skills_table.add_row(
        "-", str(c.get_ability_modifier(c.dexterity)), "Stealth", "DEX"
    )
    skills_table.add_row("-", str(c.get_ability_modifier(c.wisdom)), "Survival", "WIS")

    proficiencies = [
        v["name"] for v in c.proficiencies.values() if v["type"] != "Saving Throws"
    ]
    for n, p in enumerate(proficiencies):
        if ", " in p:
            parts = p.split(", ")
            proficiencies[n] = f"{parts[1]} {parts[0]}"

    throws_column = Layout(name="throws_column")
    throws_column.split_column(
        Layout(panel_common(insp_prof_table), size=5),
        Layout(
            panel_common(saving_throws_table, subtitle="Saving Throws"),
            size=12,
        ),
        Layout(panel_common(skills_table, subtitle="Skills"), size=23),
        Layout(
            panel_common(
                f"[bold]Proficiencies:[/bold]\n  {', '.join(proficiencies)}\n[bold]Languages:[/bold]\n  {c.languages}",
                subtitle="Proficiencies and Languages",
            ),
            size=8,
        ),
    )

    hp_column = Layout(name="hp_column")

    armor_class_row = Layout(name="armor_class_row", size=3)
    armor_class_row.split_row(
        Columns(
            [
                panel_common(str(c.armor_class), subtitle="Armor Class"),
                panel_common(
                    str(sum_rolls(d20=1) + c.get_ability_modifier(c.dexterity)),
                    subtitle="Initiative",
                ),
                panel_common(str(c.speed), subtitle="Speed"),
            ],
            width=19,
        ),
    )

    max_hp_row = Layout(name="max_hp_row", size=3)
    max_hp_row.split_row(
        Columns(
            [
                panel_common(
                    str(c.get_maximum_hp(c.hd, c.level, c.constitution)),
                    subtitle="Max HP",
                ),
                panel_common(str(c.current_hp), subtitle="Current HP"),
                panel_common(str(c.temp_hp), subtitle="Temp HP"),
            ],
            width=19,
        )
    )

    hit_dice_grid = Table.grid(expand=True)
    hit_dice_grid.add_row("Total", glowing_white_text(str(c.max_hd)))
    hit_dice_grid.add_row("Hit Dice", glowing_white_text(str(c.hd) + "d"))

    death_saves_grid = Table.grid(expand=True)
    death_saves_grid.add_row("Successes", "0")
    death_saves_grid.add_row("Failures", "0")

    hit_dice_row = Layout(name="hit_dice_row", size=4)
    hit_dice_row.split_row(
        Columns(
            [
                panel_common(hit_dice_grid, subtitle="Hit Dice", width=19),
                panel_common(
                    death_saves_grid, subtitle="Death Saves", width=19 * 2 + 1
                ),
            ],
        )
    )

    equipment_table = Table(box=box.SIMPLE, expand=True)
    equipment_table.add_column("QTY")
    equipment_table.add_column("ITEM")
    equipment_table.add_column("COST")
    equipment_table.add_column("WEIGHT")
    for item in c.inventory:
        equipment_table.add_row(
            str(item.quantity),
            str(item.name),
            f"{item.cost['quantity']}{item.cost['unit']}",
            str(item.weight),
        )

    equipment_row = Layout(equipment_table, name="equipment_row")

    money_table = Table(box=box.SIMPLE, expand=True)
    money_table.add_column("QTY")
    money_table.add_column("COIN")

    for coin, qty in c.wealth_detailed.items():
        money_table.add_row(str(qty), coin)

    money_row = Layout(money_table, name="money_row")

    hp_column.split_column(
        armor_class_row,
        max_hp_row,
        hit_dice_row,
        Layout(panel_common(money_row, subtitle="Money"), size=11),
        panel_common(equipment_row, subtitle="Equipment"),
    )

    personality_column = Layout(name="personality_column")

    features = [v["name"] for v in c.class_features.values()]
    personality_column.split_column(
        panel_common(c.personality, subtitle="Personality Traits"),
        panel_common(c.ideals, subtitle="Ideals"),
        panel_common(c.bonds, subtitle="Bonds"),
        panel_common(c.flaws, subtitle="Flaws"),
        panel_common("\n".join(features), subtitle="Features"),
    )

    base_stats_column = get_base_stats_column(c)

    layout.split_row(
        Layout(base_stats_column, size=10),
        Layout(throws_column, size=43),
        Layout(hp_column, size=60),
        Layout(personality_column, size=56),
    )

    return layout


def get_spell_table(c: Character, level: int):
    table = Table(box=box.SIMPLE)
    table.add_column("PREP")
    table.add_column("SPELL")
    table.add_column("DMG TYPE")

    spells_prepared = {s.index for s in c.spells_prepared}
    for spell in c.spells_known:
        if spell.level != level:
            continue
        if spell.damage:
            damage_type = spell.damage.get("damage_type", {}).get("name", "N/A")
        else:
            damage_type = "N/A"
        if spell.index in spells_prepared:
            table.add_row("Y", spell.name, damage_type)

    return table


def get_spells(c: Character) -> RenderableType:
    layout = Layout(name="spells")

    layout.split_column(
        Columns(
            [
                panel_common(get_spell_table(c, 1), subtitle="Level 1 Spells"),
                panel_common(get_spell_table(c, 2), subtitle="Level 2 Spells"),
            ]
        )
    )

    return layout


def render(c: Character):
    console = Console()
    width = console.size.width

    header = get_header(c, width=width)
    stats = get_stats(c, width=width)
    spells = get_spells(c)

    layout = Layout()

    layout.split_column(
        Layout(header, size=6),
        Layout(stats, size=48),
        Layout(spells, size=12),
        Layout(
            panel_common(c.lore, subtitle="Lore"),
            name="About",
            size=len(c.lore.splitlines(keepends=True)) + 2,
        ),
    )

    with console.pager(styles=True):
        console.print(layout, height=300)
