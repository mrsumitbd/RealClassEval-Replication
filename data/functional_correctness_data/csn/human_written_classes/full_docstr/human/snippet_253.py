import urllib.parse
import os
from tibiapy.utils import convert_line_breaks, parse_tibiacom_content
from tibiapy.errors import InvalidContentError
from tibiapy.models import BoostableBosses, BoostedCreatures, BossEntry, Creature, CreatureEntry, CreaturesSection

class BoostableBossesParser:
    """Parser for the boostable bosses section of Tibia.com."""

    @classmethod
    def from_content(cls, content: str) -> BoostableBosses:
        """Create an instance of the class from the html content of the boostable bosses library's page.

        Parameters
        ----------
        content:
            The HTML content of the page.

        Returns
        -------
            The Boostable Bosses section.

        Raises
        ------
        InvalidContent
            If content is not the HTML of a creature library's page.

        """
        try:
            parsed_content = parse_tibiacom_content(content)
            boosted_creature_table = parsed_content.select_one('div.TableContainer')
            boosted_creature_text = boosted_creature_table.select_one('div.Text')
            if not boosted_creature_text or 'Boosted' not in boosted_creature_text.text:
                raise InvalidContentError('content is not from the boostable bosses section.')
            boosted_boss_tag = boosted_creature_table.select_one('b')
            boosted_boss_image = boosted_creature_table.select_one('img')
            image_url = urllib.parse.urlparse(boosted_boss_image['src'])
            boosted_boss = BossEntry(name=boosted_boss_tag.text, identifier=os.path.basename(image_url.path).replace('.gif', ''))
            list_table = parsed_content.find('div', style=lambda v: v and 'display: table' in v)
            entries_container = list_table.find_all('div', style=lambda v: v and 'float: left' in v)
            entries = []
            for entry_container in entries_container:
                name = entry_container.text.strip()
                image = entry_container.select_one('img')
                image_url = urllib.parse.urlparse(image['src'])
                identifier = os.path.basename(image_url.path).replace('.gif', '')
                entries.append(BossEntry(name=name, identifier=identifier))
            return BoostableBosses(boosted_boss=boosted_boss, bosses=entries)
        except (AttributeError, ValueError) as e:
            raise InvalidContentError("content is not the boosted boss's library", e) from e

    @classmethod
    def boosted_boss_from_header(cls, content: str) -> BossEntry:
        """Get the boosted boss from any Tibia.com page.

        Parameters
        ----------
        content:
            The HTML content of a Tibia.com page.

        Returns
        -------
            The boosted boss of the day.

        Raises
        ------
        InvalidContent
            If content is not the HTML of a Tibia.com's page.

        """
        return BoostedCreaturesParser.from_header(content).boss