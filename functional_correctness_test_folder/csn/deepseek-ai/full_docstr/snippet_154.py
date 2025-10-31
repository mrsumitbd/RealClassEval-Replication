
import xml.etree.ElementTree as ET
from .tds import TDSCatalog


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
        self.name = element_node.get('name', '')
        self.href = element_node.get('{http://www.w3.org/1999/xlink}href', '')
        self.title = element_node.get(
            '{http://www.w3.org/1999/xlink}title', '')
        self._base_url = base_url

    def __str__(self):
        '''Return a string representation of the catalog reference.'''
        return f"CatalogRef(name='{self.name}', href='{self.href}', title='{self.title}')"

    def follow(self):
        '''Follow the catalog reference and return a new :class:`TDSCatalog`.
        Returns
        -------
        TDSCatalog
            The referenced catalog
        '''
        return TDSCatalog(self._base_url + self.href)
