
import importlib
import pkgutil
from typing import Any, Dict, List, Optional


class AWSComponentRegistry:
    '''
    Class responsible for discovering and managing AWS components from the diagrams package.
    Encapsulates the component discovery, caching and lookup functionality.
    '''

    def __init__(self):
        # Cache the discovered data
        self._categories: Optional[List[str]] = None
        self._components: Optional[Dict[str, List[str]]] = None
        self._aliases: Optional[Dict[str, str]] = None

    def _discover_categories(self) -> List[str]:
        if self._categories is not None:
            return self._categories

        categories = []
        try:
            import diagrams.aws as aws_pkg
        except Exception:
            self._categories = []
            return []

        for _, name, is_pkg in pkgutil.iter_modules(aws_pkg.__path__):
            if is_pkg:
                categories.append(name)
        self._categories = categories
        return categories

    def _discover_components(self) -> Dict[str, List[str]]:
        if self._components is not None:
            return self._components

        components: Dict[str, List[str]] = {}
        categories = self._discover_categories()

        for category in categories:
            try:
                mod = importlib.import_module(f"diagrams.aws.{category}")
            except Exception:
                continue

            comp_names: List[str] = []
            for _, module_name, is_pkg in pkgutil.iter_modules(mod.__path__):
                if is_pkg:
                    continue
                full_mod_name = f"diagrams.aws.{category}.{module_name}"
                try:
                    module = importlib.import_module(full_mod_name)
                except Exception:
                    continue

                # Find classes that subclass AWSComponent
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type):
                        try:
                            from diagrams.aws.aws_component import AWSComponent
                        except Exception:
                            continue
                        if issubclass(attr, AWSComponent) and attr is not AWSComponent:
                            comp_names.append(attr_name)
            components[category] = comp_names
        self._components = components
        return components

    def _build_aliases(self) -> Dict[str, str]:
        if self._aliases is not None:
            return self._aliases

        aliases: Dict[str, str] = {}
        components = self._discover_components()
        for category, names in components.items():
            for name in names:
                aliases[name] = f"diagrams.aws.{category}.{name}"
        self._aliases = aliases
        return aliases

    def get_node(self, node_type: str) -> Any:
        """
        Return the class object for the given node_type.
        node_type can be a fully qualified name or a simple alias.
        """
        # If fully qualified, try to import directly
        if "." in node_type:
            try:
                module_path, class_name = node_type.rsplit(".", 1)
                module = importlib.import_module(module_path)
                return getattr(module, class_name)
            except Exception:
                pass

        # Otherwise, look up alias
        aliases = self._build_aliases()
        if node_type not in aliases:
            raise KeyError(f"Unknown node type: {node_type}")

        fq_name = aliases[node_type]
        module_path, class_name = fq_name.rsplit(".", 1)
        module = importlib.import_module(module_path)
        return getattr(module, class_name)

    def list_available_components(self, category: Optional[str] = None) -> Dict[str, List[str]]:
        """
        Return a dictionary mapping categories to lists of component names.
        If a category is specified, only that category is returned.
        """
        components = self._discover_components()
        if category:
            return {category: components.get(category, [])}
        return components
