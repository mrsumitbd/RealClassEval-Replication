
import requests
from xml.etree import ElementTree as ET


class CatalogRef:

    def __init__(self, base_url, element_node):
        self.base_url = base_url
        self.element_node = element_node
        self.catalog_url = self._resolve_catalog_url()

    def __str__(self):
        return f"CatalogRef: {self.catalog_url}"

    def follow(self):
        try:
            response = requests.get(self.catalog_url)
            response.raise_for_status()
            return ET.fromstring(response.content)
        except requests.exceptions.RequestException as e:
            print(f"Error following catalog reference: {e}")
            return None

    def _resolve_catalog_url(self):
        catalog_url = self.element_node.attrib.get('href')
        if not catalog_url.startswith('http'):
            catalog_url = self.base_url + catalog_url
        return catalog_url
