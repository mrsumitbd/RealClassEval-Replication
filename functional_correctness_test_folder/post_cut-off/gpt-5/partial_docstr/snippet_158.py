from typing import List, Dict, Any, Optional
import importlib
import inspect
import pkgutil


class AWSComponentRegistry:
    '''
    Class responsible for discovering and managing AWS components from the diagrams package.
    Encapsulates the component discovery, caching and lookup functionality.
    '''

    def __init__(self):
        self._categories: List[str] = []
        self._components: Dict[str, List[str]] = {}
        self._aliases: Dict[str, str] = {}
        self._class_by_qualname: Dict[str, Any] = {}

        try:
            self._aws_pkg = importlib.import_module("diagrams.aws")
            self._aws_base = importlib.import_module("diagrams.aws._AWS")._AWS
        except Exception:
            self._aws_pkg = None
            self._aws_base = None

        if self._aws_pkg and self._aws_base:
            self._categories = self._discover_categories()
            self._components = self._discover_components()
            self._aliases = self._build_aliases()

    def _discover_categories(self) -> List[str]:
        if not self._aws_pkg:
            return []
        categories: List[str] = []
        try:
            for modinfo in pkgutil.iter_modules(self._aws_pkg.__path__):
                name = modinfo.name
                # Skip private and meta modules
                if name.startswith("_"):
                    continue
                categories.append(name)
        except Exception:
            return []
        return sorted(categories)

    def _discover_components(self) -> Dict[str, List[str]]:
        components: Dict[str, List[str]] = {}
        if not (self._aws_pkg and self._aws_base):
            return components

        for category in self._categories:
            try:
                module = importlib.import_module(f"diagrams.aws.{category}")
            except Exception:
                continue

            class_names: List[str] = []
            for _, obj in inspect.getmembers(module, inspect.isclass):
                # Ensure class comes from this module and is a subclass of AWS base
                if getattr(obj, "__module__", "") != module.__name__:
                    continue
                try:
                    if issubclass(obj, self._aws_base) and obj is not self._aws_base:
                        class_name = obj.__name__
                        class_names.append(class_name)
                        qual = f"aws.{category}.{class_name}"
                        self._class_by_qualname[qual] = obj
                except Exception:
                    continue

            if class_names:
                components[category] = sorted(class_names)

        return components

    def _build_aliases(self) -> Dict[str, str]:
        aliases: Dict[str, str] = {}

        def norm(s: str) -> str:
            return "".join(ch for ch in s.lower() if ch.isalnum() or ch == ".")

        for category, class_names in self._components.items():
            for cls_name in class_names:
                qual = f"aws.{category}.{cls_name}"
                # Aliases
                keys = set()
                keys.add(norm(cls_name))
                keys.add(norm(f"{category}.{cls_name}"))
                keys.add(norm(f"aws.{category}.{cls_name}"))
                # Also allow with dashes/underscores removed already by norm
                for k in keys:
                    aliases[k] = qual

        return aliases

    def get_node(self, node_type: str) -> Any:
        if not node_type:
            raise ValueError("node_type must be a non-empty string")

        # Try direct accesses: fully qualified
        candidates = []

        # Normalize
        n = "".join(ch for ch in node_type.strip().lower()
                    if ch.isalnum() or ch == ".")

        # Exact fully qualified provided by user variations
        # If user provided class name only
        candidates.append(n)
        # If user provided something like compute.ec2
        if not n.startswith("aws."):
            candidates.append(f"aws.{n}")

        # Attempt alias resolve
        for key in candidates:
            if key in self._aliases:
                qual = self._aliases[key]
                cls = self._class_by_qualname.get(qual)
                if cls is not None:
                    return cls

        # As a last resort, if user passes fully qualified with original casing
        # like aws.compute.EC2
        if node_type.startswith("aws.") and node_type.count(".") == 2:
            cls = self._class_by_qualname.get(node_type)
            if cls is not None:
                return cls

        # Try to match raw class name ignoring package (e.g., "EC2")
        raw = "".join(ch for ch in node_type.lower() if ch.isalnum())
        if raw in self._aliases:
            qual = self._aliases[raw]
            cls = self._class_by_qualname.get(qual)
            if cls is not None:
                return cls

        raise KeyError(f"Unknown AWS node type: {node_type}")

    def list_available_components(self, category: str = None) -> Dict[str, List[str]]:
        if not category:
            return {k: v[:] for k, v in self._components.items()}
        # Normalize category name
        cat = category.strip().lower()
        if cat in self._components:
            return {cat: self._components[cat][:]}
        # Allow some normalization (e.g., 'Compute' -> 'compute')
        if cat in set(self._categories):
            return {cat: self._components.get(cat, [])[:]}

        raise KeyError(f"Unknown AWS category: {category}")
