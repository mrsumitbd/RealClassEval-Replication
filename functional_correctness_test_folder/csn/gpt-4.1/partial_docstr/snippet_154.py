
import urllib.parse
import xml.etree.ElementTree as ET


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
        self.href = element_node.attrib.get(
            'xlink:href') or element_node.attrib.get('href')
        if self.href is None:
            raise ValueError(
                "catalogRef element missing 'href' or 'xlink:href' attribute")
        self.resolved_url = urllib.parse.urljoin(base_url, self.href)

    def __str__(self):
        return f"CatalogRef(href='{self.href}', resolved_url='{self.resolved_url}')"

    def follow(self):
        '''
        Returns the resolved URL of the referenced catalog.
        '''
        return self.resolved_url
