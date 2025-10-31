
class CatalogRef:

    def __init__(self, base_url, element_node):
        self.base_url = base_url
        self.element_node = element_node

    def __str__(self):
        return f"CatalogRef(base_url={self.base_url}, element_node={self.element_node})"

    def follow(self):
        import xml.etree.ElementTree as ET
        import urllib.request
        import os

        # Extract the href attribute from the element_node
        href = self.element_node.get('href')

        # Construct the full URL to the referenced catalog
        catalog_url = os.path.join(self.base_url, href)

        # Fetch the catalog file
        with urllib.request.urlopen(catalog_url) as response:
            catalog_data = response.read()

        # Parse the catalog data
        catalog_root = ET.fromstring(catalog_data)

        return catalog_root
