
import xml.etree.ElementTree as ET
from urllib.parse import urljoin


class CatalogRef:

    def __init__(self, base_url, element_node):
        '''
        Initialize the catalogRef object.
        Parameters
        ----------
        base_url : str
            URL to the base catalog that owns this reference
        element_node : :class:`~xml.etree.ElementTree.Element`
            An :class:`~xml.etree.ElementTree.Element` representing a catalogRef node
        '''
        self.base_url = base_url
        self.element_node = element_node
        self.href = element_node.attrib.get('href')

    def __str__(self):
        return f"CatalogRef to {self.href}"

    def follow(self):
        catalog_url = urljoin(self.base_url, self.href)
        try:
            return ET.parse(catalog_url).getroot()
        except ET.ParseError as e:
            raise ValueError(f"Failed to parse catalog at {catalog_url}: {e}")
