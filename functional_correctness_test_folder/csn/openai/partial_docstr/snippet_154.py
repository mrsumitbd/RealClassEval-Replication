
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET


class CatalogRef:
    """
    Represents a <catalogRef> element in an XML catalog.
    """

    def __init__(self, base_url, element_node):
        """
        Initialize the catalogRef object.

        Parameters
        ----------
        base_url : str
            URL to the base catalog that owns this reference
        element_node : xml.etree.ElementTree.Element
            An Element representing a catalogRef node
        """
        self.base_url = base_url
        self.element_node = element_node
        # The href attribute contains the relative or absolute URL of the referenced catalog
        self.href = element_node.get("href")
        if self.href is None:
            raise ValueError(
                "catalogRef element must have an 'href' attribute")

    def __str__(self):
        return f"CatalogRef(href={self.href})"

    def follow(self):
        """
        Resolve the href relative to the base URL, fetch the referenced catalog,
        parse it, and return the root Element.

        Returns
        -------
        xml.etree.ElementTree.Element
            The root element of the referenced catalog.

        Raises
        ------
        RuntimeError
            If the referenced catalog cannot be fetched or parsed.
        """
        # Resolve the full URL
        full_url = urllib.parse.urljoin(self.base_url, self.href)

        try:
            with urllib.request.urlopen(full_url) as response:
                data = response.read()
        except Exception as exc:
            raise RuntimeError(
                f"Failed to fetch catalog at {full_url}") from exc

        try:
            root = ET.fromstring(data)
        except ET.ParseError as exc:
            raise RuntimeError(
                f"Failed to parse catalog XML from {full_url}") from exc

        return root
