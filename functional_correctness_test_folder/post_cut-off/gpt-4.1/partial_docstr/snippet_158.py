
from typing import List, Dict, Any
import importlib
import pkgutil
import inspect


class AWSComponentRegistry:
    '''
    Class responsible for discovering and managing AWS components from the diagrams package.
    Encapsulates the component discovery, caching and lookup functionality.
    '''

    def __init__(self):
        self._categories = self._discover_categories()
        self._components = self._discover_components()
        self._aliases = self._build_aliases()

    def _discover_categories(self) -> List[str]:
        try:
            aws_pkg = importlib.import_module("diagrams.aws")
        except ImportError:
            return []
        categories = []
        for _, name, ispkg in pkgutil.iter_modules(aws_pkg.__path__):
            if ispkg:
                categories.append(name)
        return sorted(categories)

    def _discover_components(self) -> Dict[str, List[str]]:
        components = {}
        for category in self._categories:
            try:
                mod = importlib.import_module(f"diagrams.aws.{category}")
            except ImportError:
                continue
            comps = []
            for name, obj in inspect.getmembers(mod, inspect.isclass):
                # Only include classes defined in this module
                if obj.__module__ == mod.__name__:
                    comps.append(name)
            if comps:
                components[category] = sorted(comps)
        return components

    def _build_aliases(self) -> Dict[str, str]:
        aliases = {}
        for category, comps in self._components.items():
            for comp in comps:
                key = f"{category}.{comp}".lower()
                aliases[key] = f"{category}.{comp}"
                aliases[comp.lower()] = f"{category}.{comp}"
        return aliases

    def get_node(self, node_type: str) -> Any:
        key = node_type.lower()
        if key not in self._aliases:
            raise ValueError(
                f"Component '{node_type}' not found in AWS registry.")
        full_name = self._aliases[key]
        category, comp = full_name.split(".")
        try:
            mod = importlib.import_module(f"diagrams.aws.{category}")
            cls = getattr(mod, comp)
            return cls
        except (ImportError, AttributeError):
            raise ValueError(f"Component '{node_type}' could not be loaded.")

    def list_available_components(self, category: str = None) -> Dict[str, List[str]]:
        if category is None:
            return self._components.copy()
        if category not in self._components:
            raise ValueError(
                f"Category '{category}' not found in AWS registry.")
        return {category: self._components[category][:]}
