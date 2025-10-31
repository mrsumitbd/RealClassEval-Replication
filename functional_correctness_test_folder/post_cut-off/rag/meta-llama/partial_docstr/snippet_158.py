
import importlib
import pkgutil
from typing import Any, Dict, List


class AWSComponentRegistry:
    '''
    Class responsible for discovering and managing AWS components from the diagrams package.
    Encapsulates the component discovery, caching and lookup functionality.
    '''

    def __init__(self):
        '''Initialize the registry with discovered components and aliases'''
        self.categories = self._discover_categories()
        self.components = self._discover_components()
        self.aliases = self._build_aliases()
        self.cache = {}

    def _discover_categories(self) -> List[str]:
        '''Dynamically discover all AWS categories from the diagrams package'''
        diagrams_package = importlib.import_module('diagrams.aws')
        return [category.name for category in pkgutil.iter_modules(diagrams_package.__path__) if not category.ispkg]

    def _discover_components(self) -> Dict[str, List[str]]:
        '''Dynamically discover all available AWS components by category'''
        components = {}
        for category in self.categories:
            category_module = importlib.import_module(
                f'diagrams.aws.{category}')
            components[category] = [
                component.name for component in pkgutil.iter_modules(category_module.__path__)]
        return components

    def _build_aliases(self) -> Dict[str, str]:
        '''Build aliases dictionary by analyzing available components'''
        aliases = {}
        for category, component_list in self.components.items():
            for component in component_list:
                alias = f'{category.lower()}-{component.lower().replace("_", "-")}'
                aliases[alias] = f'{category}.{component}'
        return aliases

    def get_node(self, node_type: str) -> Any:
        '''Get AWS component class using dynamic discovery with caching'''
        if node_type in self.cache:
            return self.cache[node_type]

        if node_type in self.aliases:
            node_type = self.aliases[node_type]

        category, component = node_type.rsplit('.', 1)
        category_module = importlib.import_module(f'diagrams.aws.{category}')
        component_class = getattr(category_module, component)
        self.cache[node_type] = component_class
        return component_class

    def list_available_components(self, category: str = None) -> Dict[str, List[str]]:
        '''List all available AWS components and their aliases'''
        if category:
            return {category: self.components.get(category, [])}
        return self.components
