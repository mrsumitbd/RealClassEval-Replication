
import importlib
import inspect
import pkgutil
from typing import Any, Dict, List, Optional

# The diagrams package is expected to be installed in the environment.
# Import it lazily to avoid import errors when the registry is not used.
try:
    import diagrams
except Exception:  # pragma: no cover
    diagrams = None  # type: ignore


class AWSComponentRegistry:
    """
    Class responsible for discovering and managing AWS components from the diagrams package.
    Encapsulates the component discovery, caching and lookup functionality.
    """

    def __init__(self):
        """Initialize the registry with discovered components and aliases."""
        # Cache for component classes: {component_name: class}
        self._component_cache: Dict[str, Any] = {}
        # Mapping of alias -> component_name
        self._aliases: Dict[str, str] = {}
        # Mapping of category -> list of component names
        self._components_by_category: Dict[str, List[str]] = {}

        # Discover categories and components
        self._categories = self._discover_categories()
        self._components_by_category = self._discover_components()
        self._aliases = self._build_aliases()

    def _discover_categories(self) -> List[str]:
        """Dynamically discover all AWS categories from the diagrams package."""
        if diagrams is None:
            return []

        categories: List[str] = []
        # diagrams.aws is a package; iterate its submodules
        aws_pkg = diagrams.aws
        for _, mod_name, is_pkg in pkgutil.iter_modules(aws_pkg.__path__):
            if is_pkg:
                categories.append(mod_name)
        return categories

    def _discover_components(self) -> Dict[str, List[str]]:
        """Dynamically discover all available AWS components by category."""
        if diagrams is None:
            return {}

        components_by_category: Dict[str, List[str]] = {}
        for category in self._categories:
            try:
                mod = importlib.import_module(f"diagrams.aws.{category}")
            except Exception:
                continue

            component_names: List[str] = []
            for name, obj in inspect.getmembers(mod, inspect.isclass):
                # Only consider classes that are defined in this module
                if obj.__module__ != mod.__name__:
                    continue
                # Skip the base AWSComponent class itself
                if name == "AWSComponent":
                    continue
                component_names.append(name)
            components_by_category[category] = component_names
        return components_by_category

    def _build_aliases(self) -> Dict[str, str]:
        """Build aliases dictionary by analyzing available components."""
        if diagrams is None:
            return {}

        aliases: Dict[str, str] = {}
        for category, names in self._components_by_category.items():
            for name in names:
                try:
                    mod = importlib.import_module(f"diagrams.aws.{category}")
                    cls = getattr(mod, name)
                except Exception:
                    continue

                # The diagrams library may expose an `alias` attribute
                # or a list of aliases via `aliases`.  Handle both.
                alias_attr = getattr(cls, "alias", None)
                if alias_attr:
                    if isinstance(alias_attr, (list, tuple)):
                        for a in alias_attr:
                            aliases[a] = name
                    else:
                        aliases[alias_attr] = name

                # Some components use `aliases` attribute
                aliases_attr = getattr(cls, "aliases", None)
                if aliases_attr:
                    if isinstance(aliases_attr, (list, tuple)):
                        for a in aliases_attr:
                            aliases[a] = name
                    else:
                        aliases[aliases_attr] = name

        return aliases

    def get_node(self, node_type: str) -> Any:
        """
        Get AWS component class using dynamic discovery with caching.

        Parameters
        ----------
        node_type : str
            The component name or an alias.

        Returns
        -------
        class
            The component class.

        Raises
        ------
        KeyError
            If the component cannot be found.
        """
        if node_type in self._component_cache:
            return self._component_cache[node_type]

        # Resolve alias if present
        component_name = node_type
        if node_type in self._aliases:
            component_name = self._aliases[node_type]

        # Search for the component in all categories
        for category, names in self._components_by_category.items():
            if component_name in names:
                try:
                    mod = importlib.import_module(f"diagrams.aws.{category}")
                    cls = getattr(mod, component_name)
                    self._component_cache[node_type] = cls
                    return cls
                except Exception:
                    continue

        raise KeyError(f"Component '{node_type}' not found in diagrams.aws")

    def list_available_components(self, category: Optional[str] = None) -> Dict[str, List[str]]:
        """
        List all available AWS components and their aliases.

        Parameters
        ----------
        category : str, optional
            If provided, only return components for this category.

        Returns
        -------
        dict
            Mapping of category -> list of component names.
        """
        if category:
            return {category: self._components_by_category.get(category, [])}
        return dict(self._components_by_category)
