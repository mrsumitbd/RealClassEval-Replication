
from __future__ import annotations

import importlib
import pkgutil
from typing import Any, Dict, List, Optional

# The diagrams package is expected to be installed in the environment.
# We import it lazily to avoid import errors when the registry is not used.
try:
    import diagrams
except Exception:  # pragma: no cover
    diagrams = None  # type: ignore


class AWSComponentRegistry:
    """
    Class responsible for discovering and managing AWS components from the diagrams package.
    Encapsulates the component discovery, caching and lookup functionality.
    """

    def __init__(self) -> None:
        """Initialize the registry with discovered components and aliases."""
        # Cache for component classes: component name -> class
        self._component_classes: Dict[str, Any] = {}
        # Mapping from component name to alias
        self._aliases: Dict[str, str] = {}
        # Mapping from category to list of component names
        self._components: Dict[str, List[str]] = {}
        # Simple cache for get_node lookups
        self._cache: Dict[str, Any] = {}

        # Discover categories, components and build aliases
        self._components = self._discover_components()
        self._aliases = self._build_aliases()

    def _discover_categories(self) -> List[str]:
        """Dynamically discover all AWS categories from the diagrams package."""
        if diagrams is None:
            return []

        categories: List[str] = []
        aws_pkg = diagrams.aws
        for _, name, is_pkg in pkgutil.iter_modules(aws_pkg.__path__):
            if is_pkg:
                categories.append(name)
        return categories

    def _discover_components(self) -> Dict[str, List[str]]:
        """Dynamically discover all available AWS components by category."""
        components: Dict[str, List[str]] = {}
        if diagrams is None:
            return components

        for category in self._discover_categories():
            module_name = f"diagrams.aws.{category}"
            try:
                module = importlib.import_module(module_name)
            except Exception:
                continue

            comp_names: List[str] = []
            for attr_name in dir(module):
                if attr_name.startswith("_"):
                    continue
                attr = getattr(module, attr_name)
                if isinstance(attr, type):
                    # Ensure the class is defined in this module (or submodule)
                    if attr.__module__.startswith(module_name):
                        comp_names.append(attr_name)
                        self._component_classes[attr_name] = attr
            components[category] = sorted(comp_names)
        return components

    def _build_aliases(self) -> Dict[str, str]:
        """Build aliases dictionary by analyzing available components."""
        aliases: Dict[str, str] = {}
        for comp_name in self._component_classes:
            alias = comp_name.lower()
            aliases[alias] = comp_name
        return aliases

    def get_node(self, node_type: str) -> Any:
        """Get AWS component class using dynamic discovery with caching."""
        if node_type in self._cache:
            return self._cache[node_type]

        # Direct lookup by component name
        comp_cls = self._component_classes.get(node_type)
        if comp_cls:
            self._cache[node_type] = comp_cls
            return comp_cls

        # Alias lookup
        comp_name = self._aliases.get(node_type.lower())
        if comp_name:
            comp_cls = self._component_classes.get(comp_name)
            if comp_cls:
                self._cache[node_type] = comp
