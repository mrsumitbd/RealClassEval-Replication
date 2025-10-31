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
        from urllib.parse import urljoin

        if not isinstance(base_url, str) or not base_url:
            raise ValueError("base_url must be a non-empty string")
        self.base_url = base_url
        self.element = element_node

        # Common xlink namespace attr names
        xlink_href = '{http://www.w3.org/1999/xlink}href'
        xlink_title = '{http://www.w3.org/1999/xlink}title'

        # Extract href, accommodating both xlink and non-namespaced variants
        self.href = (
            (element_node.get(xlink_href) if element_node is not None else None)
            or (element_node.get('href') if element_node is not None else None)
        )

        # Extract a human-readable title or name
        self.title = (
            (element_node.get(xlink_title) if element_node is not None else None)
            or (element_node.get('title') if element_node is not None else None)
            or (element_node.get('name') if element_node is not None else None)
        )

        if not self.href:
            raise ValueError(
                "catalogRef element is missing href/xlink:href attribute")

        # Precompute absolute URL
        self._resolved_url = urljoin(self.base_url, self.href)

    def __str__(self):
        return self.title or self._resolved_url

    def follow(self):
        return self._resolved_url
