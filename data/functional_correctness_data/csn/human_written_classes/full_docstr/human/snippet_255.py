from tibiapy.models import BoostableBosses, BoostedCreatures, BossEntry, Creature, CreatureEntry, CreaturesSection
from tibiapy.errors import InvalidContentError
import urllib.parse
from tibiapy.utils import convert_line_breaks, parse_tibiacom_content

class CreaturesSectionParser:
    """Parser for the creatures section in the library from Tibia.com."""

    @classmethod
    def boosted_creature_from_header(cls, content: str) -> CreatureEntry:
        """Get the boosted creature from any Tibia.com page.

        Parameters
        ----------
        content:
            The HTML content of a Tibia.com page.

        Returns
        -------
            The boosted creature of the day.

        Raises
        ------
        InvalidContent
            If content is not the HTML of a Tibia.com's page.

        """
        return BoostedCreaturesParser.from_header(content).creature

    @classmethod
    def from_content(cls, content: str) -> CreaturesSection:
        """Create an instance of the class from the html content of the creature library's page.

        Parameters
        ----------
        content:
            The HTML content of the page.

        Returns
        -------
            The creatures section from Tibia.com.

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
                raise InvalidContentError('content is not from the creatures section.')
            boosted_creature_link = boosted_creature_table.select_one('a')
            url = urllib.parse.urlparse(boosted_creature_link['href'])
            query = urllib.parse.parse_qs(url.query)
            boosted_creature = CreatureEntry(name=boosted_creature_link.text, identifier=query['race'][0])
            list_table = parsed_content.find('div', style=lambda v: v and 'display: table' in v)
            entries_container = list_table.find_all('div', style=lambda v: v and 'float: left' in v)
            entries = []
            for entry_container in entries_container:
                name = entry_container.text.strip()
                link = entry_container.select_one('a')
                url = urllib.parse.urlparse(link['href'])
                query = urllib.parse.parse_qs(url.query)
                entries.append(CreatureEntry(name=name, identifier=query['race'][0]))
            return CreaturesSection(boosted_creature=boosted_creature, creatures=entries)
        except (AttributeError, ValueError) as e:
            raise InvalidContentError("content is not the creature's library", e) from e