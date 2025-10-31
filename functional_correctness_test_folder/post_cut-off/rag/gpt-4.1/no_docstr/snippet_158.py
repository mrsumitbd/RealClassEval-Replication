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
        self._categories = self._discover_categories()
        self._components = self._discover_components()
        self._aliases = self._build_aliases()
        self._node_cache = {}

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
        return sorted(categories)

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
                components[category] = sorted(comp_list)
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
        if node_type_lc in self._node_cache:
            return self._node_cache[node_type_lc]
        # Try direct match
        if node_type_lc in self._aliases:
            full_name = self._aliases[node_type_lc]
            category, comp = full_name.split(".", 1)
            try:
                mod = importlib.import_module(f"diagrams.aws.{category}")
                cls = getattr(mod, comp)
                self._node_cache[node_type_lc] = cls
                return cls
            except (ImportError, AttributeError):
                pass
        # Try to parse node_type as "Category.Component"
        if "." in node_type:
            category, comp = node_type.split(".", 1)
            try:
                mod = importlib.import_module(
                    f"diagrams.aws.{category.lower()}")
                cls = getattr(mod, comp)
                self._node_cache[node_type_lc] = cls
                return cls
            except (ImportError, AttributeError):
                pass
        raise ValueError(f"Unknown AWS component: {node_type}")

    def list_available_components(self, category: str = None) -> Dict[str, List[str]]:
        '''List all available AWS components and their aliases'''
        if category:
            category = category.lower()
            for cat in self._components:
                if cat.lower() == category:
                    return {cat: self._components[cat]}
            return {}
        return dict(self._components)
