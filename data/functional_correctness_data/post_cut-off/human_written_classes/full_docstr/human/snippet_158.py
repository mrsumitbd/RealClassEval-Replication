import logging
from typing import Any, Dict, List, Union
import inspect
import importlib
import pkgutil
from diagrams import aws

class AWSComponentRegistry:
    """
    Class responsible for discovering and managing AWS components from the diagrams package.
    Encapsulates the component discovery, caching and lookup functionality.
    """

    def __init__(self):
        """Initialize the registry with discovered components and aliases"""
        self._component_cache = {}
        self.categories = self._discover_categories()
        self.components = self._discover_components()
        self.aliases = self._build_aliases()

    def _discover_categories(self) -> List[str]:
        """Dynamically discover all AWS categories from the diagrams package"""
        categories = []
        try:
            for _, name, is_pkg in pkgutil.iter_modules(aws.__path__):
                if not is_pkg and (not name.startswith('_')):
                    categories.append(name)
        except Exception as e:
            logging.warning(f'Failed to discover AWS categories: {e}')
            return []
        return categories

    def _discover_components(self) -> Dict[str, List[str]]:
        """Dynamically discover all available AWS components by category"""
        components = {}
        for category in self.categories:
            try:
                module = importlib.import_module(f'diagrams.aws.{category}')
                components[category] = [name for name, obj in inspect.getmembers(module) if inspect.isclass(obj) and (not name.startswith('_'))]
            except ImportError:
                continue
        return components

    def _build_aliases(self) -> Dict[str, str]:
        """Build aliases dictionary by analyzing available components"""
        aliases = {}
        aliases.update({'users': 'Users', 'user': 'Users', 'client': 'Users', 'clients': 'Users', 'internet': 'Internet', 'web': 'Internet', 'mobile': 'Mobile'})
        for _, component_list in self.components.items():
            for component in component_list:
                aliases[component.lower()] = component
                clean_name = component.replace('Service', '').replace('Amazon', '').replace('AWS', '')
                if clean_name != component:
                    aliases[clean_name.lower()] = component
                if component.isupper():
                    aliases[component.lower()] = component
        return aliases

    def get_node(self, node_type: str) -> Any:
        """Get AWS component class using dynamic discovery with caching"""
        if node_type in self._component_cache:
            return self._component_cache[node_type]
        normalized = node_type.lower()
        canonical_name = self.aliases.get(normalized, node_type)
        for category, component_list in self.components.items():
            try:
                module = importlib.import_module(f'diagrams.aws.{category}')
                if canonical_name in component_list:
                    component = getattr(module, canonical_name)
                    self._component_cache[node_type] = component
                    return component
                for component_name in component_list:
                    if component_name.lower() == canonical_name.lower():
                        component = getattr(module, component_name)
                        self._component_cache[node_type] = component
                        return component
            except ImportError:
                continue
        raise ValueError(f"Component '{node_type}' not found in available AWS components")

    def list_available_components(self, category: str=None) -> Dict[str, List[str]]:
        """List all available AWS components and their aliases"""
        if category:
            return {category: self.components.get(category, [])}
        return self.components