
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

    def _discover_categories(self) -> List[str]:
        '''Dynamically discover all AWS categories from the diagrams package'''
        categories = []
        for _, name, _ in pkgutil.iter_modules(['diagrams.aws']):
            categories.append(name)
        return categories

    def _discover_components(self) -> Dict[str, List[str]]:
        '''Dynamically discover all available AWS components by category'''
        components = {}
        for category in self.categories:
            module = importlib.import_module(f'diagrams.aws.{category}')
            components[category] = [name for name in dir(module) if not name.startswith(
                '_') and not callable(getattr(module, name))]
        return components

    def _build_aliases(self) -> Dict[str, str]:
        '''Build aliases dictionary by analyzing available components'''
        aliases = {}
        for category, component_list in self.components.items():
            for component in component_list:
                aliases[component.lower(
                )] = f'diagrams.aws.{category}.{component}'
        return aliases

    def get_node(self, node_type: str) -> Any:
        '''Get AWS component class using dynamic discovery with caching'''
        node_type_lower = node_type.lower()
        if node_type_lower in self.aliases:
            module_path = self.aliases[node_type_lower]
            module_name, class_name = module_path.rsplit('.', 1)
            module = importlib.import_module(module_name)
            return getattr(module, class_name)
        raise ValueError(
            f"Component '{node_type}' not found in the AWS component registry.")

    def list_available_components(self, category: str = None) -> Dict[str, List[str]]:
        '''List all available AWS components and their aliases'''
        if category:
            if category in self.components:
                return {category: self.components[category]}
            else:
                raise ValueError(
                    f"Category '{category}' not found in the AWS component registry.")
        return self.components
