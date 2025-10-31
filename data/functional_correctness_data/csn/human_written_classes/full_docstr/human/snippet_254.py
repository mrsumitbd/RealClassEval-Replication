from tibiapy.models import BoostableBosses, BoostedCreatures, BossEntry, Creature, CreatureEntry, CreaturesSection
from tibiapy.utils import convert_line_breaks, parse_tibiacom_content
from typing import Optional
from tibiapy.builders import CreatureBuilder

class CreatureParser:
    """Parser for creatures."""
    _valid_elements = ('ice', 'fire', 'earth', 'poison', 'death', 'holy', 'physical', 'energy')

    @classmethod
    def from_content(cls, content: str) -> Optional[Creature]:
        """Create an instance of the class from the html content of the creature library's page.

        Parameters
        ----------
        content:
            The HTML content of the page.

        Returns
        -------
            The creature contained in the page.

        """
        try:
            parsed_content = parse_tibiacom_content(content)
            _, content_container = parsed_content.find_all('div', style=lambda v: v and 'position: relative' in v)
            title_container, description_container = content_container.select('div')
            title = title_container.select_one('h2')
            name = title.text.strip()
            img = title_container.select_one('img')
            img_url = img['src']
            race = img_url.split('/')[-1].replace('.gif', '')
            builder = CreatureBuilder().name(name).identifier(race)
            convert_line_breaks(description_container)
            paragraph_tags = description_container.select('p')
            paragraphs = [p.text for p in paragraph_tags]
            builder.description('\n'.join(paragraphs[:-2]).strip())
            hp_text = paragraphs[-2]
            cls._parse_hp_text(builder, hp_text)
            exp_text = paragraphs[-1]
            cls._parse_exp_text(builder, exp_text)
            return builder.build()
        except ValueError:
            return None

    @classmethod
    def _parse_exp_text(cls, builder: CreatureBuilder, exp_text: str) -> None:
        """Parse the experience text, containing dropped loot and adds it to the creature.

        Parameters
        ----------
        builder: :class:`CreatureBuilder`
            The builder where data will be stored to.
        exp_text: :class:`str`
            The text containing experience.

        """
        if (m := EXP_PATTERN.search(exp_text)):
            builder.experience(int(m.group(1)))
        if (m := LOOT_PATTERN.search(exp_text)):
            builder.loot(m.group(1))

    @classmethod
    def _parse_hp_text(cls, builder: CreatureBuilder, hp_text: str) -> None:
        """Parse the text containing the creature's hitpoints, containing weaknesses, immunities and more and adds it.

        Parameters
        ----------
        builder: :class:`CreatureBuilder`
            The builder where data will be stored to.
        hp_text: :class:`str`
            The text containing hitpoints.

        """
        m = HP_PATTERN.search(hp_text)
        if m:
            builder.hitpoints(int(m.group(1)))
        m = IMMUNE_PATTERN.search(hp_text)
        immune = []
        if m:
            immune.extend(cls._parse_elements(m.group(1)))
        if 'cannot be paralysed' in hp_text:
            immune.append('paralyze')
        if 'sense invisible' in hp_text:
            immune.append('invisible')
        builder.immune_to(immune)
        if (m := WEAK_PATTERN.search(hp_text)):
            builder.weak_against(cls._parse_elements(m.group(1)))
        if (m := STRONG_PATTERN.search(hp_text)):
            builder.strong_against(cls._parse_elements(m.group(1)))
        if (m := MANA_COST.search(hp_text)):
            builder.mana_cost(int(m.group(1)))
            if 'summon or convince' in hp_text:
                builder.convinceable(True)
                builder.summonable(True)
            if 'cannot be summoned' in hp_text:
                builder.convinceable(True)
            if 'cannot be convinced' in hp_text:
                builder.summonable(True)

    @classmethod
    def _parse_elements(cls, text: str) -> list[str]:
        """Parse the elements found in a string, adding them to the collection.

        Parameters
        ----------
        text: :class:`str`
            The text containing the elements.

        """
        return [element for element in cls._valid_elements if element in text]