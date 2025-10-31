from typing import Any, Dict, List, Optional
import importlib
import inspect
import pkgutil
import re
from functools import lru_cache


class AWSComponentRegistry:
    '''
    Class responsible for discovering and managing AWS components from the diagrams package.
    Encapsulates the component discovery, caching and lookup functionality.
    '''

    def __init__(self):
        '''Initialize the registry with discovered components and aliases'''
        self._available = False
        self._categories: List[str] = []
        # components[category][name] = class
        self._components: Dict[str, Dict[str, type]] = {}
        # aliases[alias] = "category.name"
        self._aliases: Dict[str, str] = {}
        # cache for quick get_node resolutions
        self._cache: Dict[str, type] = {}

        try:
            self._aws_pkg = importlib.import_module("diagrams.aws")
            self._aws_base: Optional[type] = None
            try:
                self._aws_base = getattr(importlib.import_module(
                    "diagrams.aws.aws"), "AWS", None)
            except Exception:
                self._aws_base = None
            self._categories = self._discover_categories()
            self._components = self._discover_components()
            self._aliases = self._build_aliases()
            self._available = True
        except Exception:
            # diagrams not available or discovery failed
            self._available = False
            self._aws_pkg = None
            self._aws_base = None

    def _discover_categories(self) -> List[str]:
        '''Dynamically discover all AWS categories from the diagrams package'''
        if not self._aws_pkg or not hasattr(self._aws_pkg, "__path__"):
            return []

        categories: List[str] = []
        for mod in pkgutil.iter_modules(self._aws_pkg.__path__):
            name = mod.name
            # Skip internal modules (e.g., __pycache__, version, pkg internals)
            if name.startswith("_"):
                continue
            # The top-level aws base module is "aws", which we do not treat as a category
            if name == "aws":
                continue
            categories.append(name)
        categories.sort()
        return categories

    def _discover_components(self) -> Dict[str, List[str]]:
        '''Dynamically discover all available AWS components by category'''
        result: Dict[str, Dict[str, type]] = {}
        for cat in self._categories:
            fqmn = f"diagrams.aws.{cat}"
            try:
                mod = importlib.import_module(fqmn)
            except Exception:
                continue

            comp_map: Dict[str, type] = {}
            for attr_name in dir(mod):
                if attr_name.startswith("_"):
                    continue
                obj = getattr(mod, attr_name)
                if not inspect.isclass(obj):
                    continue
                # Only accept classes declared in diagrams.aws.* modules
                obj_mod = getattr(obj, "__module__", "")
                if not obj_mod.startswith("diagrams.aws."):
                    continue
                # Filter by subclass of AWS base if available, otherwise keep heuristics
                if self._aws_base is not None:
                    try:
                        if not issubclass(obj, self._aws_base) or obj is self._aws_base:
                            continue
                        comp_map[obj.__name__] = obj
                    except Exception:
                        continue
                else:
                    # Fallback heuristic: public classes in the category module
                    comp_map[obj.__name__] = obj

            if comp_map:
                result[cat] = comp_map

        # Convert to desired return type: Dict[str, List[str]] of names
        # but we also keep the class map internally
        self._components = result
        return {cat: sorted(list(names.keys())) for cat, names in result.items()}

    def _build_aliases(self) -> Dict[str, str]:
        '''Build aliases dictionary by analyzing available components'''
        aliases: Dict[str, str] = {}

        def camel_to_snake(name: str) -> str:
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
            s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
            return s2.lower()

        for category, comp_map in self._components.items():
            for name in comp_map.keys():
                qualified = f"{category}.{name}"

                # Primary keys
                for key in (
                    name,  # class name
                    f"{category}.{name}",
                    f"aws.{category}.{name}",
                ):
                    aliases[key] = qualified

                # Lowercase and snake_case aliases
                lower = name.lower()
                snake = camel_to_snake(name)

                for key in (
                    lower,
                    snake,
                    f"{category}.{lower}",
                    f"{category}.{snake}",
                    f"aws.{category}.{lower}",
                    f"aws.{category}.{snake}",
                ):
                    aliases[key] = qualified

        return aliases

    @lru_cache(maxsize=1024)
    def _resolve(self, node_type: str) -> type:
        # Normalize input
        key = node_type.strip()
        if key.startswith("aws."):
            key = key[4:]

        # Try direct matches first
        if key in self._aliases:
            category, name = self._aliases[key].split(".", 1)
            return self._components[category][name]

        # If looks like "category.Name"
        if "." in key:
            parts = key.split(".")
            if len(parts) == 2:
                category, name = parts
                if category in self._components and name in self._components[category]:
                    return self._components[category][name]

        # Try case-insensitive class name search across categories
        lname = key.lower()
        # collect candidates to handle duplicates gracefully (prefer first discovered category)
        for category, comp_map in self._components.items():
            for name, cls in comp_map.items():
                if name.lower() == lname:
                    return cls

        # Try snake_case to CamelCase
        candidate = "".join(part.capitalize()
                            for part in re.split(r"[_\s\-]+", lname) if part)
        if candidate:
            for category, comp_map in self._components.items():
                if candidate in comp_map:
                    return comp_map[candidate]

        raise KeyError(f"AWS component not found for '{node_type}'")

    def get_node(self, node_type: str) -> Any:
        '''Get AWS component class using dynamic discovery with caching'''
        if not self._available:
            raise RuntimeError(
                "diagrams package is not available or AWS components could not be discovered")
        if not isinstance(node_type, str) or not node_type.strip():
            raise ValueError("node_type must be a non-empty string")

        try:
            return self._resolve(node_type)
        except KeyError as e:
            raise ValueError(str(e)) from None

    def list_available_components(self, category: str = None) -> Dict[str, List[str]]:
        '''List all available AWS components and their aliases'''
        if not self._available:
            return {}

        def camel_to_snake(name: str) -> str:
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
            s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
            return s2.lower()

        def entries_for(cat: str) -> List[str]:
            names = set()
            for name in self._components.get(cat, {}).keys():
                names.add(name)
                names.add(name.lower())
                names.add(camel_to_snake(name))
                names.add(f"{cat}.{name}")
                names.add(f"{cat}.{name.lower()}")
                names.add(f"{cat}.{camel_to_snake(name)}")
                names.add(f"aws.{cat}.{name}")
                names.add(f"aws.{cat}.{name.lower()}")
                names.add(f"aws.{cat}.{camel_to_snake(name)}")
            return sorted(names)

        if category:
            if category.startswith("aws."):
                category = category[4:]
            if category not in self._components:
                return {}
            return {category: entries_for(category)}

        result: Dict[str, List[str]] = {}
        for cat in sorted(self._components.keys()):
            result[cat] = entries_for(cat)
        return result
