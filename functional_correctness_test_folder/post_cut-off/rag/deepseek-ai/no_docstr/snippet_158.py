
from typing import List, Dict, Any
import importlib
import pkgutil
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
            import diagrams.aws as aws
            categories = []
            for module_info in pkgutil.iter_modules(aws.__path__):
                categories.append(module_info.name)
            return categories
        except ImportError:
            return []

    def _discover_components(self) -> Dict[str, List[str]]:
        '''Dynamically discover all available AWS components by category'''
        components = {}
        for category in self._categories:
            try:
                module = importlib.import_module(f"diagrams.aws.{category}")
                category_components = []
                for name, obj in module.__dict__.items():
                    if isinstance(obj, type) and hasattr(obj, '__module__') and obj.__module__ == module.__name__:
                        category_components.append(name)
                components[category] = category_components
            except ImportError:
                continue
        return components

    def _build_aliases(self) -> Dict[str, str]:
        '''Build aliases dictionary by analyzing available components'''
        aliases = {}
        for category, components in self._components.items():
            for component in components:
                aliases[component.lower(
                )] = f"diagrams.aws.{category}.{component}"
        return aliases

    @lru_cache(maxsize=None)
    def get_node(self, node_type: str) -> Any:
        '''Get AWS component class using dynamic discovery with caching'''
        if node_type in self._aliases:
            module_path, class_name = self._aliases[node_type].rsplit('.', 1)
            module = importlib.import_module(module_path)
            return getattr(module, class_name)
        raise ValueError(f"Component '{node_type}' not found in AWS registry")

    def list_available_components(self, category: str = None) -> Dict[str, List[str]]:
        '''List all available AWS components and their aliases'''
        if category:
            return {category: self._components.get(category, [])}
        return self._components
