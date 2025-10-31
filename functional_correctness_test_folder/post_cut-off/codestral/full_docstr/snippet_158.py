
import importlib
from typing import List, Dict, Any


class AWSComponentRegistry:
    '''
    Class responsible for discovering and managing AWS components from the diagrams package.
    Encapsulates the component discovery, caching and lookup functionality.
    '''

    def __init__(self):
        '''Initialize the registry with discovered components and aliases'''
        self._categories = self._discover_categories()
        self._components = self._discover_components()
        self._aliases = self._build_aliases()
        self._node_cache = {}

    def _discover_categories(self) -> List[str]:
        '''Dynamically discover all AWS categories from the diagrams package'''
        aws_module = importlib.import_module('diagrams.aws')
        categories = [name for name in dir(
            aws_module) if not name.startswith('_')]
        return categories

    def _discover_components(self) -> Dict[str, List[str]]:
        '''Dynamically discover all available AWS components by category'''
        components = {}
        for category in self._categories:
            category_module = importlib.import_module(
                f'diagrams.aws.{category}')
            components[category] = [name for name in dir(
                category_module) if not name.startswith('_')]
        return components

    def _build_aliases(self) -> Dict[str, str]:
        '''Build aliases dictionary by analyzing available components'''
        aliases = {}
        for category, components in self._components.items():
            for component in components:
                aliases[component.lower()] = f'{category}.{component}'
        return aliases

    def get_node(self, node_type: str) -> Any:
        '''Get AWS component class using dynamic discovery with caching'''
        if node_type in self._node_cache:
            return self._node_cache[node_type]

        if node_type.lower() in self._aliases:
            category, component = self._aliases[node_type.lower()].split('.')
            module = importlib.import_module(f'diagrams.aws.{category}')
            node_class = getattr(module, component)
            self._node_cache[node_type] = node_class
            return node_class

        raise ValueError(f'Node type {node_type} not found')

    def list_available_components(self, category: str = None) -> Dict[str, List[str]]:
        '''List all available AWS components and their aliases'''
        if category:
            if category in self._components:
                return {category: self._components[category]}
            else:
                raise ValueError(f'Category {category} not found')
        return self._components
