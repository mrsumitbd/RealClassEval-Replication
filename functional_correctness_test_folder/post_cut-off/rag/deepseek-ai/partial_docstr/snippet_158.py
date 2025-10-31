
import importlib
from typing import Any, Dict, List
from diagrams import aws


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
        return [attr for attr in dir(aws) if not attr.startswith('_')]

    def _discover_components(self) -> Dict[str, List[str]]:
        '''Dynamically discover all available AWS components by category'''
        components = {}
        for category in self._categories:
            module = importlib.import_module(
                f'diagrams.aws.{category.lower()}')
            components[category] = [attr for attr in dir(
                module) if not attr.startswith('_')]
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
        if node_type in self._aliases:
            category, comp = self._aliases[node_type].split('.')
            module = importlib.import_module(
                f'diagrams.aws.{category.lower()}')
            return getattr(module, comp)
        raise ValueError(f"Component '{node_type}' not found in AWS registry")

    def list_available_components(self, category: str = None) -> Dict[str, List[str]]:
        '''List all available AWS components and their aliases'''
        if category:
            if category not in self._categories:
                raise ValueError(f"Category '{category}' not found")
            return {category: self._components[category]}
        return self._components
