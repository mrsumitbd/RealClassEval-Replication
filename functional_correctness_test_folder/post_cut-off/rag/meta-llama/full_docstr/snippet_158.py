
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
        diagrams_module = importlib.import_module('diagrams.aws')
        return [module_name for _, module_name, _ in pkgutil.iter_modules(diagrams_module.__path__)]

    def _discover_components(self) -> Dict[str, List[str]]:
        '''Dynamically discover all available AWS components by category'''
        components = {}
        for category in self.categories:
            module_name = f'diagrams.aws.{category}'
            module = importlib.import_module(module_name)
            components[category] = [cls_name for cls_name in dir(
                module) if not cls_name.startswith('_')]
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

        try:
            category, component = self.aliases[node_type].split('.')
        except KeyError:
            raise ValueError(f'Unknown AWS component: {node_type}')

        module_name = f'diagrams.aws.{category}'
        module = importlib.import_module(module_name)
        component_class = getattr(module, component)
        self.cache[node_type] = component_class
        return component_class

    def list_available_components(self, category: str = None) -> Dict[str, List[str]]:
        '''List all available AWS components and their aliases'''
        if category:
            return {category: self.components.get(category, [])}
        return self.components
