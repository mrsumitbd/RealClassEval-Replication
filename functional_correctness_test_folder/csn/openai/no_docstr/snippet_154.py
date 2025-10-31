
import urllib.parse


class CatalogRef:
    def __init__(self, base_url, element_node):
        """
        Create a reference to a catalog entry.

        Parameters
        ----------
        base_url : str
            The base URL used to resolve relative references.
        element_node : xml.etree.ElementTree.Element or lxml.etree._Element
            The XML element that contains the reference information.
        """
        self.base_url = base_url
        self.element_node = element_node

    def __str__(self):
        """
        Return a human‑readable representation of the element.
        """
        attrs = ' '.join(f'{k}="{v}"' for k,
                         v in self.element_node.attrib.items())
        return f'<{self.element_node.tag} {attrs}>'

    def follow(self):
        """
        Resolve the reference to an absolute URL.

        Returns
        -------
        str
            The absolute URL obtained by joining the base URL with the
            element's ``href`` attribute.

        Raises
        ------
        ValueError
            If the element does not contain an ``href`` attribute.
        """
        href = self.element_node.attrib.get('href')
        if href is None:
            raise ValueError('Element does not contain an href attribute')
        return urllib.parse.urljoin(self.base_url, href)
