
import importlib
import pkgutil
from typing import Any, Dict, List, Optional


class AWSComponentRegistry:
    '''
    Class responsible for discovering and managing AWS components from the diagrams package.
    Encapsulates the component discovery, caching and lookup functionality.
    '''

    def __init__(self):
        '''Initialize the registry with discovered components and aliases'''
        self._components = self._discover_components()
        self._aliases = self._build_aliases()
        self._node_cache = {}

    def _discover_categories(self) -> List[str]:
        '''Dynamically discover all AWS categories from the diagrams package'''
        categories = []
        diagrams_package = importlib.import_module('diagrams.aws')
        for _, module_name, _ in pkgutil.iter_modules(diagrams_package.__path__):
            if not module_name.startswith('_'):
                categories.append(module_name)
        return categories

    def _discover_components(self) -> Dict[str, List[str]]:
        '''Dynamically discover all available AWS components by category'''
        components = {}
        for category in self._discover_categories():
            module = importlib.import_module(f'diagrams.aws.{category}')
            components[category] = [name for name in dir(
                module) if not name.startswith('_') and name[0].isupper()]
        return components

    def _build_aliases(self) -> Dict[str, str]:
        '''Build aliases dictionary by analyzing available components'''
        aliases = {}
        for category, components in self._components.items():
            for component in components:
                alias = f'{category}.{component}'
                aliases[alias.lower()] = f'diagrams.aws.{category}.{component}'
        return aliases

    def get_node(self, node_type: str) -> Any:
        '''Get AWS component class using dynamic discovery with caching'''
        if node_type in self._node_cache:
            return self._node_cache[node_type]

        node_type_lower = node_type.lower()
        if node_type_lower in self._aliases:
            module_path, class_name = self._aliases[node_type_lower].rsplit(
                '.', 1)
            module = importlib.import_module(module_path)
            node_class = getattr(module, class_name)
            self._node_cache[node_type] = node_class
            return node_class

        raise ValueError(
            f"AWS component '{node_type}' not found in the registry")

    def list_available_components(self, category: str = None) -> Dict[str, List[str]]:
        '''List all available AWS components and their aliases'''
        if category:
            if category in self._components:
                return {category: self._components[category]}
            raise ValueError(f"Category '{category}' not found")
        return self._components
