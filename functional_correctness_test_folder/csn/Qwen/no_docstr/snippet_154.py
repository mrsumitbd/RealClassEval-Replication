
import requests
from xml.etree import ElementTree as ET


class CatalogRef:

    def __init__(self, base_url, element_node):
        self.base_url = base_url
        self.element_node = element_node
        self.href = self.element_node.attrib.get('href', '')

    def __str__(self):
        return f"CatalogRef(base_url={self.base_url}, href={self.href})"

    def follow(self):
        if not self.href:
            raise ValueError("No href attribute found in the element node.")
        full_url = f"{self.base_url}/{self.href}"
        response = requests.get(full_url)
        response.raise_for_status()
        return ET.fromstring(response.content)
