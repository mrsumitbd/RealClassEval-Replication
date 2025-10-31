from typing import Any, Dict, List, Optional
import importlib
import inspect
import pkgutil


class AWSComponentRegistry:
    '''
    Class responsible for discovering and managing AWS components from the diagrams package.
    Encapsulates the component discovery, caching and lookup functionality.
    '''

    def __init__(self):
        '''Initialize the registry with discovered components and aliases'''
        self._available = False
        self._categories: List[str] = []
        self._components: Dict[str, List[str]] = {}
        self._class_index: Dict[str, Any] = {}
        self._aliases: Dict[str, str] = {}
        self._node_cache: Dict[str, Any] = {}
        try:
            self._aws_pkg = importlib.import_module("diagrams.aws")
            self._available = True
        except Exception:
            self._aws_pkg = None
            self._available = False
        if self._available:
            self._categories = self._discover_categories()
            self._components = self._discover_components()
            self._aliases = self._build_aliases()

    @staticmethod
    def _normalize_key(key: str) -> str:
        if key is None:
            return ""
        k = key.strip()
        if k.lower().startswith("aws."):
            k = k[4:]
        # normalize separators and remove them to be lenient
        for ch in [".", "/", ":", "-", "_", " "]:
            k = k.replace(ch, "")
        return k.lower()

    def _discover_categories(self) -> List[str]:
        '''Dynamically discover all AWS categories from the diagrams package'''
        if not self._available:
            return []
        categories: List[str] = []
        try:
            for m in pkgutil.iter_modules(self._aws_pkg.__path__):
                name = m.name
                if not name or name.startswith("_"):
                    continue
                categories.append(name)
        except Exception:
            return []
        return sorted(set(categories))

    def _discover_components(self) -> Dict[str, List[str]]:
        '''Dynamically discover all available AWS components by category'''
        components: Dict[str, List[str]] = {}
        if not self._available:
            return components

        for category in self._categories:
            module_name = f"diagrams.aws.{category}"
            try:
                mod = importlib.import_module(module_name)
            except Exception:
                continue

            comp_names: List[str] = []
            for attr_name, obj in vars(mod).items():
                if not inspect.isclass(obj):
                    continue
                # Prefer classes defined in the module or its submodules
                if not obj.__module__.startswith(mod.__name__):
                    continue
                # Heuristic to identify diagram node classes (diagrams nodes have _icon_dir)
                if not hasattr(obj, "_icon_dir"):
                    continue
                comp_names.append(attr_name)
                canonical = f"{category}.{attr_name}"
                self._class_index[canonical] = obj

            if comp_names:
                components[category] = sorted(set(comp_names))
        return components

    def _build_aliases(self) -> Dict[str, str]:
        '''Build aliases dictionary by analyzing available components'''
        aliases: Dict[str, str] = {}
        if not self._components:
            return aliases

        # Determine which component names are unique across categories
        name_occurrences: Dict[str, int] = {}
        for _, comps in self._components.items():
            for c in comps:
                name_occurrences[c.lower()] = name_occurrences.get(
                    c.lower(), 0) + 1

        def add_alias(alias: str, canonical: str):
            norm = self._normalize_key(alias)
            if not norm:
                return
            # Do not override existing mapping to preserve first-found resolution
            if norm not in aliases:
                aliases[norm] = canonical

        for category, comps in self._components.items():
            for comp in comps:
                canonical = f"{category}.{comp}"
                # canonical forms
                add_alias(f"{category}.{comp}", canonical)
                add_alias(f"aws.{category}.{comp}", canonical)
                # alternative separators
                add_alias(f"{category}/{comp}", canonical)
                add_alias(f"{category}-{comp}", canonical)
                add_alias(f"{category}_{comp}", canonical)
                # Only component name if unique across categories
                if name_occurrences.get(comp.lower(), 0) == 1:
                    add_alias(comp, canonical)
                    add_alias(comp.lower(), canonical)
                    add_alias(comp.replace("_", "-"), canonical)
                    add_alias(comp.replace("_", ""), canonical)
        return aliases

    def get_node(self, node_type: str) -> Any:
        '''Get AWS component class using dynamic discovery with caching'''
        if not self._available:
            raise ImportError("diagrams package is not available")
        if not node_type:
            raise ValueError("node_type must be a non-empty string")

        norm = self._normalize_key(node_type)
        if norm in self._node_cache:
            return self._node_cache[norm]

        canonical: Optional[str] = self._aliases.get(norm)
        if canonical is None:
            # Try a last-resort resolution by scanning known canonical keys
            # with a normalized contains match
            for cand in self._class_index.keys():
                if self._normalize_key(cand) == norm or self._normalize_key(f"aws.{cand}") == norm:
                    canonical = cand
                    break

        if canonical is None:
            raise ValueError(f"Unknown AWS node type: {node_type}")

        cls = self._class_index.get(canonical)
        if cls is None:
            raise ValueError(f"AWS node class not found for: {node_type}")
        self._node_cache[norm] = cls
        return cls

    def list_available_components(self, category: str = None) -> Dict[str, List[str]]:
        '''List all available AWS components and their aliases'''
        if not self._available:
            return {}
        if category is None:
            return {cat: list(names) for cat, names in self._components.items()}
        # case-insensitive category match
        target = None
        cat_lower = category.lower()
        for cat in self._components.keys():
            if cat.lower() == cat_lower:
                target = cat
                break
        if target is None:
            return {}
        return {target: list(self._components.get(target, []))}
