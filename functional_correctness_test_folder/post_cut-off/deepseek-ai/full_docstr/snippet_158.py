
from typing import List, Dict, Any
import importlib
from diagrams.aws import *


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
        self._cache = {}

    def _discover_categories(self) -> List[str]:
        '''Dynamically discover all AWS categories from the diagrams package'''
        aws_module = importlib.import_module('diagrams.aws')
        categories = []
        for attr in dir(aws_module):
            if not attr.startswith('_') and attr[0].isupper():
                categories.append(attr)
        return categories

    def _discover_components(self) -> Dict[str, List[str]]:
        '''Dynamically discover all available AWS components by category'''
        components = {}
        for category in self._categories:
            try:
                category_module = importlib.import_module(
                    f'diagrams.aws.{category.lower()}')
                category_components = []
                for attr in dir(category_module):
                    if not attr.startswith('_') and attr[0].isupper():
                        category_components.append(attr)
                components[category] = category_components
            except ImportError:
                continue
        return components

    def _build_aliases(self) -> Dict[str, str]:
        '''Build aliases dictionary by analyzing available components'''
        aliases = {}
        for category, comp_list in self._components.items():
            for comp in comp_list:
                aliases[comp.lower()] = f"{category}.{comp}"
        return aliases

    def get_node(self, node_type: str) -> Any:
        '''Get AWS component class using dynamic discovery with caching'''
        if node_type in self._cache:
            return self._cache[node_type]

        if node_type in self._aliases:
            category, comp = self._aliases[node_type].split('.')
            module = importlib.import_module(
                f'diagrams.aws.{category.lower()}')
            node_class = getattr(module, comp)
            self._cache[node_type] = node_class
            return node_class

        for category, comp_list in self._components.items():
            if node_type in comp_list:
                module = importlib.import_module(
                    f'diagrams.aws.{category.lower()}')
                node_class = getattr(module, node_type)
                self._cache[node_type] = node_class
                return node_class

        raise ValueError(f"Component {node_type} not found")

    def list_available_components(self, category: str = None) -> Dict[str, List[str]]:
        '''List all available AWS components and their aliases'''
        if category:
            return {category: self._components.get(category, [])}
        return self._components
