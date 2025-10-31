
import importlib
from typing import List, Dict, Any
from functools import lru_cache


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

    def _discover_categories(self) -> List[str]:
        '''Dynamically discover all AWS categories from the diagrams package'''
        try:
            diagrams_aws = importlib.import_module('diagrams.aws')
            categories = [name for name in dir(
                diagrams_aws) if not name.startswith('_')]
            return categories
        except ImportError:
            return []

    def _discover_components(self) -> Dict[str, List[str]]:
        '''Dynamically discover all available AWS components by category'''
        components = {}
        for category in self._categories:
            try:
                module = importlib.import_module(f'diagrams.aws.{category}')
                category_components = [name for name in dir(
                    module) if not name.startswith('_')]
                components[category] = category_components
            except ImportError:
                continue
        return components

    def _build_aliases(self) -> Dict[str, str]:
        '''Build aliases dictionary by analyzing available components'''
        aliases = {}
        for category, components in self._components.items():
            for component in components:
                aliases[component.lower()] = f"{category}.{component}"
        return aliases

    @lru_cache(maxsize=None)
    def get_node(self, node_type: str) -> Any:
        '''Get AWS component class using dynamic discovery with caching'''
        if node_type in self._aliases:
            category, component = self._aliases[node_type].split('.')
            try:
                module = importlib.import_module(f'diagrams.aws.{category}')
                return getattr(module, component)
            except (ImportError, AttributeError):
                pass
        return None

    def list_available_components(self, category: str = None) -> Dict[str, List[str]]:
        '''List all available AWS components and their aliases'''
        if category:
            return {category: self._components.get(category, [])}
        return self._components
