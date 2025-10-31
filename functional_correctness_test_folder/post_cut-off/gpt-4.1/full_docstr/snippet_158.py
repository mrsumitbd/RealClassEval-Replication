
import importlib
import pkgutil
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
        self._class_cache = {}

    def _discover_categories(self) -> List[str]:
        '''Dynamically discover all AWS categories from the diagrams package'''
        categories = []
        try:
            aws_pkg = importlib.import_module("diagrams.aws")
        except ImportError:
            return []
        pkg_path = aws_pkg.__path__
        for _, name, ispkg in pkgutil.iter_modules(pkg_path):
            if ispkg:
                categories.append(name)
        return categories

    def _discover_components(self) -> Dict[str, List[str]]:
        '''Dynamically discover all available AWS components by category'''
        components = {}
        for category in self._categories:
            try:
                mod = importlib.import_module(f"diagrams.aws.{category}")
            except ImportError:
                continue
            comp_list = []
            for attr in dir(mod):
                if attr.startswith("_"):
                    continue
                obj = getattr(mod, attr)
                if isinstance(obj, type):
                    comp_list.append(attr)
            if comp_list:
                components[category] = comp_list
        return components

    def _build_aliases(self) -> Dict[str, str]:
        '''Build aliases dictionary by analyzing available components'''
        aliases = {}
        for category, comps in self._components.items():
            for comp in comps:
                key = f"{category}.{comp}".lower()
                aliases[key] = f"{category}.{comp}"
                aliases[comp.lower()] = f"{category}.{comp}"
        return aliases

    def get_node(self, node_type: str) -> Any:
        '''Get AWS component class using dynamic discovery with caching'''
        node_type_lc = node_type.lower()
        if node_type_lc in self._class_cache:
            return self._class_cache[node_type_lc]
        if node_type_lc in self._aliases:
            full_name = self._aliases[node_type_lc]
            category, comp = full_name.split(".")
            try:
                mod = importlib.import_module(f"diagrams.aws.{category}")
                cls = getattr(mod, comp)
                self._class_cache[node_type_lc] = cls
                return cls
            except (ImportError, AttributeError):
                pass
        # Try to parse as category.component
        if "." in node_type:
            category, comp = node_type.split(".", 1)
            try:
                mod = importlib.import_module(f"diagrams.aws.{category}")
                cls = getattr(mod, comp)
                self._class_cache[node_type_lc] = cls
                return cls
            except (ImportError, AttributeError):
                pass
        raise ValueError(
            f"Component '{node_type}' not found in AWS diagrams package.")

    def list_available_components(self, category: str = None) -> Dict[str, List[str]]:
        '''List all available AWS components and their aliases'''
        if category:
            category = category.lower()
            for cat in self._components:
                if cat.lower() == category:
                    return {cat: self._components[cat]}
            return {}
        return self._components.copy()
