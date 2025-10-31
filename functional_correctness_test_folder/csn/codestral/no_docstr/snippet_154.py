
class CatalogRef:

    def __init__(self, base_url, element_node):
        self.base_url = base_url
        self.element_node = element_node

    def __str__(self):
        return f"CatalogRef(base_url={self.base_url}, element_node={self.element_node})"

    def follow(self):
        import requests
        from bs4 import BeautifulSoup

        response = requests.get(self.base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        element = soup.find(self.element_node)
        return element
