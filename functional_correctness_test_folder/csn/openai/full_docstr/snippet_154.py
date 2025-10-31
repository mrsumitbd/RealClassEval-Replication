
import urllib.parse
import urllib.request
from xml.etree import ElementTree as ET

# Assume TDSCatalog is defined elsewhere in the package.
# Import it lazily to avoid circular imports.
try:
    from .tdscatalog import TDSCatalog
except Exception:
    # Fallback: define a minimal placeholder for type checking
    class TDSCatalog:
        def __init__(self, url):
            self.url = url

        def __repr__(self):
            return f"<TDSCatalog url={self.url!r}>"


class CatalogRef:
    '''
    An object for holding catalog references obtained from a THREDDS Client Catalog.
    Attributes
    ----------
    name : str
        The name of the :class:`CatalogRef` element
    href : str
        url to the :class:`CatalogRef`'s THREDDS Client Catalog
    title : str
        Title of the :class:`CatalogRef` element
    '''

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
        self.name = element_node.get('name', '')
        self.title = element_node.get('title', '')
        href = element_node.get('href', '')
        # Resolve relative href against the base URL
        self.href = urllib.parse.urljoin(base_url, href)

    def __str__(self):
        '''Return a string representation of the catalog reference.'''
        return f"CatalogRef(name={self.name!r}, title={self.title!r}, href={self.href!r})"

    def follow(self):
        '''Follow the catalog reference and return a new :class:`TDSCatalog`.
        Returns
        -------
        TDSCatalog
            The referenced catalog
        '''
        # Let TDSCatalog handle fetching and parsing.
        return TDSCatalog(self.href)
