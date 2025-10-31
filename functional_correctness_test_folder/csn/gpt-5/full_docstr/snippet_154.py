class CatalogRef:
    '''
    An object for holding catalog references obtained from a THREDDS Client Catalog.
    Attributes
    ----------
    name : str
        The name of the CatalogRef element
    href : str
        url to the CatalogRef's THREDDS Client Catalog
    title : str
        Title of the CatalogRef element
    '''

    def __init__(self, base_url, element_node):
        '''
        Initialize the catalogRef object.
        Parameters
        ----------
        base_url : str
            URL to the base catalog that owns this reference
        element_node : xml.etree.ElementTree.Element
            An xml.etree.ElementTree.Element representing a catalogRef node
        '''
        from urllib.parse import urljoin

        if base_url is None:
            base_url = ''

        xlink_ns = 'http://www.w3.org/1999/xlink'
        # Extract attributes with namespace fallbacks
        href = (
            element_node.get(f'{{{xlink_ns}}}href')
            or element_node.get('href')
            or ''
        )
        title = (
            element_node.get(f'{{{xlink_ns}}}title')
            or element_node.get('title')
            or ''
        )
        name = element_node.get('name') or title or ''

        self.href = urljoin(base_url, href) if href else urljoin(base_url, '')
        self.title = title or name or self.href
        self.name = name or self.title

    def __str__(self):
        '''Return a string representation of the catalog reference.'''
        if self.title and self.href:
            return f'{self.title} -> {self.href}'
        return self.href or self.title or ''

    def follow(self):
        '''Follow the catalog reference and return a new TDSCatalog.
        Returns
        -------
        TDSCatalog
            The referenced catalog
        '''
        # Lazy import to avoid circular dependencies
        try:
            from .catalog import TDSCatalog
        except Exception:
            try:
                from siphon.catalog import TDSCatalog
            except Exception as exc:
                raise ImportError(
                    'TDSCatalog class could not be imported.') from exc

        return TDSCatalog(self.href)
