
from diagrams.aws import *
import importlib
import pkgutil
from typing import List, Dict, Any


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
        module = importlib.import_module('diagrams.aws')
        categories = [name for _, name,
                      ispkg in pkgutil.iter_modules(module.__path__) if ispkg]
        return categories

    def _discover_components(self) -> Dict[str, List[str]]:
        '''Dynamically discover all available AWS components by category'''
        components = {}
        for category in self.categories:
            module = importlib.import_module(f'diagrams.aws.{category}')
            components[category] = [name for name in dir(
                module) if not name.startswith('_') and name != 'Node']
        return components

    def _build_aliases(self) -> Dict[str, str]:
        '''Build aliases dictionary by analyzing available components'''
        aliases = {}
        for category, component_list in self.components.items():
            for component in component_list:
                aliases[component.lower()] = f'{category}.{component}'
        return aliases

    def get_node(self, node_type: str) -> Any:
        '''Get AWS component class using dynamic discovery with caching'''
        if node_type in self.cache:
            return self.cache[node_type]

        if node_type in self.aliases:
            category, component = self.aliases[node_type].split('.')
            module = importlib.import_module(f'diagrams.aws.{category}')
            node_class = getattr(module, component)
            self.cache[node_type] = node_class
            return node_class
        else:
            raise ValueError(f'Unknown AWS component: {node_type}')

    def list_available_components(self, category: str = None) -> Dict[str, List[str]]:
        '''List all available AWS components and their aliases'''
        if category:
            return {category: self.components.get(category, [])}
        else:
            return self.components
