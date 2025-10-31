
import importlib
import inspect
import pkgutil
from typing import Any, Dict, List, Optional

# Import the diagrams package and its aws subpackage
try:
    import diagrams
    import diagrams.aws
except Exception as exc:
    raise ImportError(
        "The 'diagrams' package is required for AWSComponentRegistry.") from exc


class AWSComponentRegistry:
    """
    Class responsible for discovering and managing AWS components from the diagrams package.
    Encapsulates the component discovery, caching and lookup functionality.
    """

    def __init__(self):
        """Initialize the registry with discovered components and aliases."""
        # Discover categories and components
        self._categories: List[str] = self._discover_categories()
        self._components: Dict[str, List[str]] = self._discover_components()
        # Build alias mapping
        self._aliases: Dict[str, str] = self._build_aliases()
        # Cache for node lookups
        self._node_cache: Dict[str, Any] = {}

    def _discover_categories(self) -> List[str]:
        """Dynamically discover all AWS categories from the diagrams package."""
        categories = []
        for _, mod_name, is_pkg in pkgutil.iter_modules(diagrams.aws.__path__):
            if is_pkg:
                categories.append(mod_name)
        return sorted(categories)

    def _discover_components(self) -> Dict[str, List[str]]:
        """Dynamically discover all available AWS components by category."""
        components: Dict[str, List[str]] = {}
        for category in self._categories:
            try:
                module = importlib.import_module(f"diagrams.aws.{category}")
            except Exception:
                continue
            # Find all classes defined in this module
            cls_names = [
                name
                for name, obj in inspect.getmembers(module, inspect.isclass)
                if obj.__module__ == module.__name__
            ]
            components[category] = sorted(cls_names)
        return components

    def _build_aliases(self) -> Dict[str, str]:
        """Build aliases dictionary by analyzing available components."""
        aliases: Dict[str, str] = {}
        for category, cls_names in self._components.items():
            for name in cls_names:
                alias = name.lower()
                # Avoid collisions: if alias already exists, keep the first one
                if alias not in aliases:
                    aliases[alias] = f"{category}.{name}"
        return aliases

    def get_node(self, node_type: str) -> Any:
        """
        Get AWS component class using dynamic discovery with caching.

        Parameters
        ----------
        node_type : str
            The component name or alias.

        Returns
        -------
        Any
            The component class.

        Raises
        ------
        KeyError
            If the component cannot be found.
        """
        # Return from cache if available
        if node_type in self._node_cache:
            return self._node_cache[node_type]

        # Resolve alias to full name
        full_name = self._aliases.get(node_type.lower(), node_type)

        # Split into category and class name
        if "." in full_name:
            category, class_name = full_name.split(".", 1)
        else:
            # Try to find the class in any category
            found = None
            for cat, names in self._components.items():
                if full_name in names:
                    category, class_name = cat, full_name
                    found = True
                    break
            if not found:
                raise KeyError(
                    f"Component '{node_type}' not found in AWS registry.")

        # Import the module and get the class
        try:
            module = importlib.import_module(f"diagrams.aws.{category}")
            component_cls = getattr(module, class_name)
        except (ImportError, AttributeError) as exc:
            raise KeyError(
                f"Component '{node_type}' could not be loaded.") from exc

        # Cache and return
        self._node_cache[node_type] = component_cls
        return component_cls

    def list_available_components(self, category: Optional[str] = None) -> Dict[str, List[str]]:
        """
        List all available AWS components and their aliases.

        Parameters
        ----------
        category : str, optional
            If provided, only return components for this category.

        Returns
        -------
        Dict[str, List[str]]
            Mapping from category to list of component names.
        """
        if category:
            if category not in self._components:
                raise KeyError(f"Category '{category}' not found.")
            return {category: self._components[category]}

        return dict(self._components)
