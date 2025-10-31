from typing import Any, Dict, List, Optional
import importlib
import inspect
import pkgutil
import re


class AWSComponentRegistry:
    '''
    Class responsible for discovering and managing AWS components from the diagrams package.
    Encapsulates the component discovery, caching and lookup functionality.
    '''

    def __init__(self):
        '''Initialize the registry with discovered components and aliases'''
        self._diagrams_available = False
        self._aws_pkg = None
        self._diagrams_node_cls = None

        try:
            self._aws_pkg = importlib.import_module("diagrams.aws")
            self._diagrams_node_cls = importlib.import_module(
                "diagrams.elements").Node
            self._diagrams_available = True
        except Exception:
            # Diagrams not available; keep registry empty but functional
            self._diagrams_available = False
            self._aws_pkg = None
            self._diagrams_node_cls = None

        self._categories: List[str] = []
        self._components_by_category: Dict[str, List[str]] = {}
        self._fqname_to_class: Dict[str, Any] = {}
        self._aliases: Dict[str, str] = {}
        self._resolve_cache: Dict[str, Any] = {}

        if self._diagrams_available:
            self._categories = self._discover_categories()
            self._components_by_category = self._discover_components()
            self._aliases = self._build_aliases()

    def _discover_categories(self) -> List[str]:
        '''Dynamically discover all AWS categories from the diagrams package'''
        if not self._diagrams_available:
            return []
        categories: List[str] = []
        try:
            for modinfo in pkgutil.iter_modules(self._aws_pkg.__path__):
                # Categories are modules under diagrams.aws (e.g., compute, storage, network)
                name = modinfo.name
                if name.startswith("_"):
                    continue
                categories.append(name)
        except Exception:
            pass
        # Keep order stable, but remove duplicates if any
        seen = set()
        ordered = []
        for c in categories:
            if c not in seen:
                ordered.append(c)
                seen.add(c)
        return ordered

    def _discover_components(self) -> Dict[str, List[str]]:
        '''Dynamically discover all available AWS components by category'''
        components: Dict[str, List[str]] = {}
        if not self._diagrams_available:
            return components

        for category in self._categories:
            module_name = f"diagrams.aws.{category}"
            try:
                mod = importlib.import_module(module_name)
            except Exception:
                continue

            names: List[str] = []
            for _, cls in inspect.getmembers(mod, inspect.isclass):
                # Only classes defined in this module or its submodules
                if not getattr(cls, "__module__", "").startswith(module_name):
                    continue
                # Must be a subclass of Node (diagrams base), exclude the base Node itself
                if self._diagrams_node_cls and not issubclass(cls, self._diagrams_node_cls):
                    continue
                # Exclude base or internal classes generally not representing icons
                if cls.__name__.startswith("_"):
                    continue
                if cls.__module__ in ("diagrams.aws.aws", "diagrams.elements"):
                    continue

                class_name = cls.__name__
                fqname = f"diagrams.aws.{category}.{class_name}"

                # Cache fqname -> class for quick resolution
                self._fqname_to_class[fqname] = cls
                names.append(class_name)

            # Deduplicate and sort component names for this category
            names = sorted(list({n for n in names}))
            if names:
                components[category] = names

        return components

    def _build_aliases(self) -> Dict[str, str]:
        '''Build aliases dictionary by analyzing available components'''
        aliases: Dict[str, str] = {}

        def normalize(s: str) -> str:
            s = s.strip().lower()
            # collapse separators and remove non-alnum except dots
            s = s.replace("::", ".")
            s = re.sub(r"[\s/_\-]+", ".", s)
            s = re.sub(r"[^\w\.]", "", s)
            return s

        def camel_to_snake(name: str) -> str:
            name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
            name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
            return name.lower()

        for category, class_names in self._components_by_category.items():
            for name in class_names:
                fq = f"diagrams.aws.{category}.{name}"

                candidates = set()

                # Raw names and simple variants
                candidates.add(name)
                candidates.add(name.lower())
                snake = camel_to_snake(name)
                candidates.add(snake)
                candidates.add(snake.replace("_", ""))

                # Dotted category variants
                candidates.add(f"{category}.{name}")
                candidates.add(f"{category}.{name}".lower())
                candidates.add(f"{category}.{snake}")
                candidates.add(f"{category}.{snake.replace('_', '')}")

                # aws prefixed
                candidates.add(f"aws.{category}.{name}")
                candidates.add(f"aws.{category}.{name}".lower())
                candidates.add(f"aws.{category}.{snake}")
                candidates.add(f"aws.{category}.{snake.replace('_', '')}")

                # full module style
                candidates.add(f"diagrams.aws.{category}.{name}")

                # Hyphenated snake case as common user input
                candidates.add(snake.replace("_", "-"))

                # Register normalized candidates if not already taken
                for cand in candidates:
                    key = normalize(cand)
                    if key and key not in aliases:
                        aliases[key] = fq

        return aliases

    def get_node(self, node_type: str) -> Any:
        '''Get AWS component class using dynamic discovery with caching'''
        if not isinstance(node_type, str):
            raise TypeError("node_type must be a string")
        if not self._diagrams_available:
            raise RuntimeError("diagrams package is not available")

        if node_type in self._resolve_cache:
            return self._resolve_cache[node_type]

        def normalize(s: str) -> str:
            s = s.strip().lower()
            s = s.replace("::", ".")
            s = re.sub(r"[\s/_\-]+", ".", s)
            s = re.sub(r"[^\w\.]", "", s)
            return s

        def camel_to_snake(name: str) -> str:
            name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
            name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
            return name.lower()

        key = normalize(node_type)

        # Direct alias match
        if key in self._aliases:
            fq = self._aliases[key]
            cls = self._fqname_to_class.get(fq)
            if cls is not None:
                self._resolve_cache[node_type] = cls
                return cls

        # Try CloudFormation-like "AWS::Service::Resource" pattern
        if "::" in node_type or key.startswith("aws."):
            parts = key.split(".")
            parts = [p for p in parts if p and p != "aws" and p != "diagrams"]
            if len(parts) >= 2:
                service = parts[-2]
                resource = parts[-1]
                combos = [
                    f"{service}.{resource}",
                    f"{service}.{camel_to_snake(resource)}",
                    f"{service}.{resource}".lower(),
                    f"{service}{resource}",
                    f"{service}_{resource}",
                    f"aws.{service}.{resource}",
                ]
                for c in combos:
                    ckey = normalize(c)
                    if ckey in self._aliases:
                        fq = self._aliases[ckey]
                        cls = self._fqname_to_class.get(fq)
                        if cls is not None:
                            self._resolve_cache[node_type] = cls
                            return cls

        # Try treating the last token as component across categories
        tokens = key.split(".")
        last = tokens[-1] if tokens else key
        # Check exact lower name
        for fq, cls in self._fqname_to_class.items():
            name = fq.split(".")[-1]
            if name.lower() == last:
                self._resolve_cache[node_type] = cls
                return cls
            snake = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
            snake = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", snake).lower()
            if snake == last or snake.replace("_", "") == last.replace(".", ""):
                self._resolve_cache[node_type] = cls
                return cls

        # Not found
        raise KeyError(f"AWS component not found for '{node_type}'")

    def list_available_components(self, category: str = None) -> Dict[str, List[str]]:
        '''List all available AWS components and their aliases'''
        if not self._diagrams_available:
            return {}

        if category is None:
            # Return a copy to avoid mutation from outside
            return {k: list(v) for k, v in self._components_by_category.items()}

        # Case-insensitive category match
        target: Optional[str] = None
        cl = (category or "").lower()
        for cat in self._components_by_category.keys():
            if cat.lower() == cl:
                target = cat
                break
        if target is None:
            return {}

        return {target: list(self._components_by_category.get(target, []))}
