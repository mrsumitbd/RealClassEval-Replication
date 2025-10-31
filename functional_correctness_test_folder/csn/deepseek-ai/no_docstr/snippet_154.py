
class CatalogRef:

    def __init__(self, base_url, element_node):
        self.base_url = base_url
        self.element_node = element_node

    def __str__(self):
        return f"CatalogRef(base_url={self.base_url}, element_node={self.element_node})"

    def follow(self):
        import requests
        url = f"{self.base_url}/{self.element_node}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
