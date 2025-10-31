
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
        self._categories = self._discover_categories()
        self._components = self._discover_components()
        self._aliases = self._build_aliases()
        self._node_cache: Dict[str, Any] = {}

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
        for category in self._categories:
            module = importlib.import_module(f'diagrams.aws.{category}')
            components[category] = [name for name in dir(
                module) if not name.startswith('_') and name[0].isupper()]
        return components

    def _build_aliases(self) -> Dict[str, str]:
        '''Build aliases dictionary by analyzing available components'''
        aliases = {}
        for category, component_list in self._components.items():
            for component in component_list:
                alias = f'{category}.{component}'
                aliases[alias.lower()] = f'{category}.{component}'
        return aliases

    def get_node(self, node_type: str) -> Any:
        '''Get AWS component class using dynamic discovery with caching'''
        if node_type in self._node_cache:
            return self._node_cache[node_type]

        normalized_type = node_type.lower()
        if normalized_type in self._aliases:
            node_type = self._aliases[normalized_type]

        category, component = node_type.split('.', 1)
        if category not in self._components or component not in self._components[category]:
            raise ValueError(f"Unknown AWS component: {node_type}")

        module = importlib.import_module(f'diagrams.aws.{category}')
        node_class = getattr(module, component)
        self._node_cache[node_type] = node_class
        return node_class

    def list_available_components(self, category: str = None) -> Dict[str, List[str]]:
        '''List all available AWS components and their aliases'''
        if category:
            if category not in self._components:
                raise ValueError(f"Unknown AWS category: {category}")
            return {category: self._components[category]}
        return self._components
