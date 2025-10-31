from urllib.parse import urljoin, urlparse

class CatalogRef:
    """
    An object for holding catalog references obtained from a THREDDS Client Catalog.

    Attributes
    ----------
    name : str
        The name of the :class:`CatalogRef` element
    href : str
        url to the :class:`CatalogRef`'s THREDDS Client Catalog
    title : str
        Title of the :class:`CatalogRef` element

    """

    def __init__(self, base_url, element_node):
        """
        Initialize the catalogRef object.

        Parameters
        ----------
        base_url : str
            URL to the base catalog that owns this reference
        element_node : :class:`~xml.etree.ElementTree.Element`
            An :class:`~xml.etree.ElementTree.Element` representing a catalogRef node

        """
        self.title = element_node.attrib['{http://www.w3.org/1999/xlink}title']
        self.name = element_node.attrib.get('name', self.title)
        href = element_node.attrib['{http://www.w3.org/1999/xlink}href']
        self.href = urljoin(base_url, href)

    def __str__(self):
        """Return a string representation of the catalog reference."""
        return str(self.title)

    def follow(self):
        """Follow the catalog reference and return a new :class:`TDSCatalog`.

        Returns
        -------
        TDSCatalog
            The referenced catalog

        """
        return TDSCatalog(self.href)
    __repr__ = __str__