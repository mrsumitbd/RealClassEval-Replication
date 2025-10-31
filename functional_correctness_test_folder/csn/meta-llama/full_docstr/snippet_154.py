
import xml.etree.ElementTree as ET
from urllib.parse import urljoin


class TDSCatalog:
    # Assuming TDSCatalog class is defined elsewhere
    pass


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
        self.name = element_node.attrib.get('name')
        self.href = urljoin(base_url, element_node.attrib.get('xlink:href'))
        self.title = element_node.attrib.get('xlink:title')

    def __str__(self):
        '''Return a string representation of the catalog reference.'''
        return f'CatalogRef: {self.name} - {self.title} ({self.href})'

    def follow(self):
        '''Follow the catalog reference and return a new :class:`TDSCatalog`.
        Returns
        -------
        TDSCatalog
            The referenced catalog
        '''
        # Assuming TDSCatalog has a constructor that accepts a URL
        return TDSCatalog(self.href)
