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
            import diagrams.aws
            aws_pkg = diagrams.aws
            for _, modname, ispkg in pkgutil.iter_modules(aws_pkg.__path__):
                if ispkg:
                    categories.append(modname)
        except Exception:
            pass
        return sorted(categories)

    def _discover_components(self) -> Dict[str, List[str]]:
        '''Dynamically discover all available AWS components by category'''
        components = {}
        try:
            import diagrams.aws
            for category in self._discover_categories():
                try:
                    mod = importlib.import_module(f"diagrams.aws.{category}")
                    names = []
                    for attr in dir(mod):
                        obj = getattr(mod, attr)
                        if isinstance(obj, type) and getattr(obj, "__module__", "") == mod.__name__:
                            names.append(attr)
                    if names:
                        components[category] = sorted(names)
                except Exception:
                    continue
        except Exception:
            pass
        return components

    def _build_aliases(self) -> Dict[str, str]:
        '''Build aliases dictionary by analyzing available components'''
        aliases = {}
        for category, comps in self._components.items():
            for comp in comps:
                key = comp.lower()
                aliases[key] = f"{category}.{comp}"
                # Add also category+comp as alias (e.g. "ec2instance" -> "compute.EC2Instance")
                aliases[(category + comp).lower()] = f"{category}.{comp}"
        return aliases

    def get_node(self, node_type: str) -> Any:
        '''Get AWS component class using dynamic discovery with caching'''
        if node_type in self._node_cache:
            return self._node_cache[node_type]
        lookup = node_type
        if lookup in self._aliases:
            lookup = self._aliases[lookup]
        if "." in lookup:
            category, comp = lookup.split(".", 1)
            try:
                mod = importlib.import_module(f"diagrams.aws.{category}")
                cls = getattr(mod, comp)
                self._node_cache[node_type] = cls
                return cls
            except Exception:
                pass
        raise ValueError(f"Unknown AWS component: {node_type}")

    def list_available_components(self, category: str = None) -> Dict[str, List[str]]:
        '''List all available AWS components and their aliases'''
        if category:
            if category in self._components:
                return {category: self._components[category]}
            else:
                return {}
        return dict(self._components)
