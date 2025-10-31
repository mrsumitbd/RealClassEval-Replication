
import xml.etree.ElementTree as ET
import urllib.parse
import urllib.request


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
        self.href = element_node.get('{http://www.w3.org/1999/xlink}href')
        self.title = element_node.get(
            '{http://www.w3.org/1999/xlink}title', '')

    def __str__(self):
        return f"CatalogRef(title='{self.title}', href='{self.href}')"

    def follow(self):
        if not self.href:
            raise ValueError("No href attribute found in catalogRef")
        absolute_url = urllib.parse.urljoin(self.base_url, self.href)
        with urllib.request.urlopen(absolute_url) as response:
            content = response.read()
        return ET.fromstring(content)
