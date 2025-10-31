
import importlib
import inspect
import pkgutil
from typing import Any, Dict, List, Tuple

# The diagrams package is optional – we import lazily to avoid import errors
try:
    import diagrams.base  # type: ignore
except Exception:
    diagrams = None  # pragma: no cover
else:
    diagrams = importlib.import_module("diagrams")  # type: ignore


class AWSComponentRegistry:
    """
    Class responsible for discovering and managing AWS components from the diagrams package.
    Encapsulates the component discovery, caching and lookup functionality.
    """

    def __init__(self):
        """Initialize the registry with discovered components and aliases"""
        # Discover categories, components and build alias mapping
        self._categories: List[str] = self._discover_categories()
        self._components: Dict[str, List[str]] = self._discover_components()
        self._aliases: Dict[str, str] = self._build_aliases()
        # Cache for node classes
        self._node_cache: Dict[str, Any] = {}

    def _discover_categories(self) -> List[str]:
        """Dynamically discover all AWS categories from the diagrams package"""
        categories: List[str] = []
        if not diagrams:
            return categories
        aws_pkg = importlib.import_module("diagrams.aws")  # type: ignore
        for _, name, is_pkg in pkgutil.iter_modules(aws_pkg.__path__):
            if is_pkg:
                categories.append(name)
        return categories

    def _discover_components(self) -> Dict[str, List[str]]:
        """Dynamically discover all available AWS components by category"""
        components: Dict[str, List[str]] = {}
        if not diagrams:
            return components
        for cat in self._categories:
            module_name = f"diagrams.aws.{cat}"
            try:
                mod = importlib.import_module(module_name)
            except Exception:
                continue
            comp_names: List[str] = []
            for attr_name in dir(mod):
                if attr_name.startswith("_"):
                    continue
                attr = getattr(mod, attr_name)
                if inspect.isclass(attr):
                    # Only include concrete Node subclasses
                    if diagrams.base and issubclass(attr, diagrams.base.Node):
                        comp_names.append(attr_name)
            components[cat] = comp_names
        return components

    def _build_aliases(self) -> Dict[str, str]:
        """Build aliases dictionary by analyzing available components"""
        aliases: Dict[str, str] = {}
        for cat, comps in self._components.items():
            for comp in comps:
                alias = comp.lower()
                aliases[alias] = comp
        return aliases

    def get_node(self, node_type: str) -> Any:
        """Get AWS component class using dynamic discovery with caching"""
        if node_type in self._node_cache:
            return self._node_cache[node_type]

        # Resolve component name from alias if necessary
        comp_name = node_type
        if node_type not in self._components.get("", []):
            comp_name = self._aliases.get(node_type, node_type)

        # Find the component in the discovered components
        for cat, comps in self._components.items():
            if comp_name in comps:
                module_name = f"diagrams.aws.{cat}"
                try:
                    mod = importlib.import_module(module_name)
                except Exception:
                    continue
                cls = getattr(mod, comp_name, None)
                if cls:
                    self._node_cache[node_type] = cls
                    return cls

        raise KeyError(
            f"Component '{node_type}' not found in AWS diagrams registry")

    def list_available_components(self, category: str = None) -> Dict[str, List[Tuple[str, str]]]:
        """
        List all available AWS components and their aliases.

        Returns a dictionary mapping category names to a list of tuples
        (component_name, alias). If ``category`` is provided, only that
        category is returned.
        """
        result: Dict[str, List[Tuple[str, str]]] = {}
        cats = [category] if category else self._categories
        for cat in cats:
            comps = self._components.get(cat, [])
            result[cat] = [(c, self._aliases.get(c.lower(), ""))
                           for c in comps]
        return result
