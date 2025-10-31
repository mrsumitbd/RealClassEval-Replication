
import boto3
from typing import List, Dict, Any


class AWSComponentRegistry:

    def __init__(self):
        self.client = boto3.client('servicecatalog')
        self.categories = self._discover_categories()
        self.components = self._discover_components()
        self.aliases = self._build_aliases()

    def _discover_categories(self) -> List[str]:
        response = self.client.list_portfolios()
        categories = [portfolio['DisplayName']
                      for portfolio in response['PortfolioDetails']]
        return categories

    def _discover_components(self) -> Dict[str, List[str]]:
        components = {}
        for category in self.categories:
            response = self.client.search_products(
                PortfolioName=category,
                Filters={'FullTextSearch': ['']}
            )
            components[category] = [product['Name']
                                    for product in response['ProductViewDetails']]
        return components

    def _build_aliases(self) -> Dict[str, str]:
        aliases = {}
        for category, products in self.components.items():
            for product in products:
                aliases[product.lower().replace(' ', '_')] = product
        return aliases

    def get_node(self, node_type: str) -> Any:
        if node_type in self.aliases:
            return self.aliases[node_type]
        else:
            raise ValueError(
                f"Node type {node_type} not found in the registry.")

    def list_available_components(self, category: str = None) -> Dict[str, List[str]]:
        if category:
            if category in self.components:
                return {category: self.components[category]}
            else:
                raise ValueError(
                    f"Category {category} not found in the registry.")
        else:
            return self.components
