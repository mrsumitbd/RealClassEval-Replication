
import xml.etree.ElementTree as ET
from urllib.parse import urljoin


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
        self.name = element_node.get('name')
        self.href = urljoin(base_url, element_node.get('xlink:href'))
        self.title = element_node.find('title').text if element_node.find(
            'title') is not None else None

    def __str__(self):
        '''Return a string representation of the catalog reference.'''
        return f"CatalogRef(name={self.name}, href={self.href}, title={self.title})"

    def follow(self):
        '''Follow the catalog reference and return a new :class:`TDSCatalog`.
        Returns
        -------
        TDSCatalog
            The referenced catalog
        '''
        from thredds_crawler.crawl import Crawl  # Assuming TDSCatalog is part of this module or similar
        crawl = Crawl(self.href)
        return crawl.catalogs[0] if crawl.catalogs else None
