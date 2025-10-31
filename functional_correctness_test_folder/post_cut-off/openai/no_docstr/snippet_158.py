
from typing import Any, Dict, List, Optional


class AWSComponentRegistry:
    """
    A very lightweight registry for AWS components.

    The registry keeps track of component categories, the components that belong
    to each category, and a simple alias mapping.  Components are represented
    by their names and can be instantiated on demand via :meth:`get_node`.
    """

    def __init__(self) -> None:
        # Internal storage for components: {category: [component_name, ...]}
        self._components: Dict[str, List[str]] = {}
        # Alias mapping: {alias: component_name}
        self._aliases: Dict[str, str] = {}
        # Cache of instantiated nodes: {component_name: instance}
        self._nodes: Dict[str, Any] = {}

    # --------------------------------------------------------------------- #
    # Discovery helpers (currently trivial – can be overridden)
    # --------------------------------------------------------------------- #
    def _discover_categories(self) -> List[str]:
        """
        Return a list of all component categories known to the registry.
        """
        return list(self._components.keys())

    def _discover_components(self) -> Dict[str, List[str]]:
        """
        Return the internal mapping of categories to component names.
        """
        return self._components

    def _build_aliases(self) -> Dict[str, str]:
        """
        Build a mapping from lower‑cased component names to the canonical
        component name.  This is useful for case‑insensitive look‑ups.
        """
        self._aliases = {
            name.lower(): name
            for names in self._components.values()
            for name in names
        }
        return self._aliases

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def get_node(self, node_type: str) -> Any:
        """
        Return an instance of the requested component.

        Parameters
        ----------
        node_type : str
            The name of the component to instantiate.  The lookup is case
            insensitive – the registry will try the exact name first and
            fall back to the alias mapping.

        Returns
        -------
        Any
            An instance of the component.  If the component has not been
            instantiated before, a new instance is created and cached.
        """
        # Resolve the canonical name
        canonical = node_type
        if canonical not in self._components.get("", []):
            canonical = self._aliases.get(node_type.lower(), node_type)

        # Instantiate lazily
        if canonical not in self._nodes:
            # For demonstration purposes we create a simple object.
            # In a real implementation this would import and instantiate
            # the actual component class.
            self._nodes[canonical] = type(canonical, (), {})()
        return self._nodes[canonical]

    def list_available_components(
        self, category: Optional[str] = None
    ) -> Dict[str, List[str]]:
        """
        List all available components, optionally filtered by category.

        Parameters
        ----------
        category : str, optional
            If provided, only components in this category are returned.

        Returns
        -------
        Dict[str, List[str]]
            Mapping of category to component names.
        """
        if category:
            return {category: self._components.get(category, [])}
        return self._components

    # --------------------------------------------------------------------- #
    # Utility methods for populating the registry
    # --------------------------------------------------------------------- #
    def register_component(self, category: str, name: str) -> None:
        """
        Register a new component under the given category.

        Parameters
        ----------
        category : str
            The category under which the component should be listed.
        name : str
            The name of the component.
        """
        self._components.setdefault(category, []).append(name)
        # Update aliases immediately
        self._aliases[name.lower()] = name
