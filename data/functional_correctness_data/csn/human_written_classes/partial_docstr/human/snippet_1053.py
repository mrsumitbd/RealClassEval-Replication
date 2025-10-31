from tibiapy.models import BoostableBosses, BoostedCreatures, BossEntry, Creature, CreatureEntry, CreaturesSection
import bs4
from tibiapy.errors import InvalidContentError

class BoostedCreaturesParser:
    """Parser for boosted creatures and bosses."""

    @classmethod
    def _parse_boosted_platform(cls, parsed_content: bs4.BeautifulSoup, tag_id: str) -> tuple[str, str]:
        img = parsed_content.select_one(f'#{tag_id}')
        name = BOOSTED_ALT.sub('', img['title']).strip()
        image_url = img['src']
        identifier = image_url.split('/')[-1].replace('.gif', '')
        return (name, identifier)

    @classmethod
    def from_header(cls, content: str) -> BoostedCreatures:
        """Parse both boosted creature and boss from the content of any section in Tibia.com.

        Parameters
        ----------
        content:
            The HTML content of the page.

        Returns
        -------
            The boosted creature and boss.

        Raises
        ------
        InvalidContent
            If content is not the HTML of a Tibia.com page.

        """
        try:
            parsed_content = bs4.BeautifulSoup(content.replace('ISO-8859-1', 'utf-8'), 'lxml', parse_only=bs4.SoupStrainer('div', attrs={'id': 'RightArtwork'}))
            creature_name, creature_identifier = cls._parse_boosted_platform(parsed_content, 'Monster')
            boss_name, boss_identifier = cls._parse_boosted_platform(parsed_content, 'Boss')
            return BoostedCreatures(creature=CreatureEntry(name=creature_name, identifier=creature_identifier), boss=BossEntry(name=boss_name, identifier=boss_identifier))
        except (TypeError, NameError, KeyError) as e:
            raise InvalidContentError('content is not from Tibia.com', e) from e