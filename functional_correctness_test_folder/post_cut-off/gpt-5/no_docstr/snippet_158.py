from typing import Any, Dict, List, Tuple, Optional
import importlib
import inspect
import pkgutil


class AWSComponentRegistry:
    def __init__(self):
        self._namespace = "diagrams.aws"
        self._categories: List[str] = self._discover_categories()
        self._components: Dict[str, List[str]] = self._discover_components()
        self._aliases: Dict[str, Tuple[str, str]] = self._build_aliases()

    def _discover_categories(self) -> List[str]:
        try:
            aws_pkg = importlib.import_module(self._namespace)
        except ModuleNotFoundError:
            return []
        paths = getattr(aws_pkg, "__path__", None)
        if not paths:
            return []
        categories: List[str] = []
        for modinfo in pkgutil.iter_modules(paths):
            # In diagrams, categories are submodules/subpackages under diagrams.aws
            name = modinfo.name
            if not name.startswith("_"):
                categories.append(name)
        categories.sort()
        return categories

    def _discover_components(self) -> Dict[str, List[str]]:
        components: Dict[str, List[str]] = {}
        for category in self._categories:
            full_module = f"{self._namespace}.{category}"
            try:
                mod = importlib.import_module(full_module)
            except Exception:
                continue
            names: List[str] = []
            for attr_name, obj in inspect.getmembers(mod, inspect.isclass):
                # Include only classes defined in this module (avoid imports)
                if obj.__module__ == full_module and not attr_name.startswith("_"):
                    names.append(attr_name)
            names.sort()
            if names:
                components[category] = names
        return components

    def _build_aliases(self) -> Dict[str, Tuple[str, str]]:
        aliases: Dict[str, Tuple[str, str]] = {}

        def norm(s: str) -> str:
            return "".join(ch for ch in s.lower() if ch.isalnum())

        # Map normalized keys to (category, component)
        # - "component"
        # - "category.component"
        # - "aws.category.component"
        # If a normalized "component" is ambiguous, prefer the first encountered but still allow category-qualified lookups
        for category, comps in self._components.items():
            for comp in comps:
                n_comp = norm(comp)
                n_cat = norm(category)
                # component only
                aliases.setdefault(n_comp, (category, comp))
                # category.component
                aliases.setdefault(f"{n_cat}.{n_comp}", (category, comp))
                # aws.category.component
                aliases.setdefault(f"aws.{n_cat}.{n_comp}", (category, comp))
        return aliases

    def get_node(self, node_type: str) -> Any:
        if not node_type or not isinstance(node_type, str):
            raise KeyError("Node type must be a non-empty string")
        key = "".join(ch for ch in node_type.lower()
                      if ch.isalnum() or ch == ".")
        # try different interpretations
        lookup_keys = [key]
        # also try removing dots for raw-component lookups
        lookup_keys.append("".join(ch for ch in key if ch.isalnum()))
        # try stripping leading aws.
        if key.startswith("aws."):
            lookup_keys.append(key[4:])
        for k in lookup_keys:
            target = self._aliases.get(k)
            if target:
                category, comp = target
                module_name = f"{self._namespace}.{category}"
                try:
                    mod = importlib.import_module(module_name)
                    cls = getattr(mod, comp)
                    return cls
                except Exception as e:
                    raise ImportError(
                        f"Failed to load {module_name}.{comp}: {e}") from e
        # If not found, build a helpful error message
        raise KeyError(f"Node type '{node_type}' not found")

    def list_available_components(self, category: str = None) -> Dict[str, List[str]]:
        if not category:
            return {cat: list(comps) for cat, comps in self._components.items()}
        # case-insensitive category match
        normalized = category.strip().lower()
        # Try direct key match
        if category in self._components:
            return {category: list(self._components[category])}
        # Try case-insensitive
        for cat in self._components:
            if cat.lower() == normalized:
                return {cat: list(self._components[cat])}
        # Not found -> empty
        return {}
