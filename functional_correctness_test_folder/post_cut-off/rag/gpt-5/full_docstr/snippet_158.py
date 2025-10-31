from typing import Any, Dict, List, Optional
import importlib
import inspect
import pkgutil
import re
from threading import RLock


class AWSComponentRegistry:
    '''
    Class responsible for discovering and managing AWS components from the diagrams package.
    Encapsulates the component discovery, caching and lookup functionality.
    '''

    def __init__(self):
        '''Initialize the registry with discovered components and aliases'''
        self._lock = RLock()
        self._class_cache: Dict[str, Any] = {}
        self._categories: List[str] = []
        self._components_by_category: Dict[str, List[str]] = {}
        self._aliases: Dict[str, str] = {}
        try:
            self._categories = self._discover_categories()
            self._components_by_category = self._discover_components()
            self._aliases = self._build_aliases()
        except Exception:
            # Be resilient if diagrams package is not available or structure is unexpected
            self._categories = []
            self._components_by_category = {}
            self._aliases = {}

    def _discover_categories(self) -> List[str]:
        '''Dynamically discover all AWS categories from the diagrams package'''
        try:
            aws_pkg = importlib.import_module('diagrams.aws')
        except Exception:
            return []
        names: List[str] = []
        try:
            # type: ignore[attr-defined]
            for modinfo in pkgutil.iter_modules(aws_pkg.__path__):
                name = modinfo.name
                if name.startswith('_'):
                    continue
                names.append(name)
        except Exception:
            # Fallback: try to use attributes on aws package
            for name in dir(aws_pkg):
                if name.startswith('_'):
                    continue
                try:
                    attr = getattr(aws_pkg, name)
                    if inspect.ismodule(attr):
                        names.append(name)
                except Exception:
                    continue
        # Unique and sorted
        return sorted(sorted(set(names)), key=str.lower)

    def _discover_components(self) -> Dict[str, List[str]]:
        '''Dynamically discover all available AWS components by category'''
        components: Dict[str, List[str]] = {}
        for category in self._categories:
            fq_module = f'diagrams.aws.{category}'
            comp_names: List[str] = []
            try:
                mod = importlib.import_module(fq_module)
            except Exception:
                components[category] = []
                continue

            # Preferred: use __all__ from the category aggregator module
            names_from_all: Optional[List[str]] = None
            try:
                all_attr = getattr(mod, '__all__', None)
                if isinstance(all_attr, (list, tuple)):
                    names_from_all = [str(x) for x in all_attr]
            except Exception:
                names_from_all = None

            if names_from_all:
                for nm in names_from_all:
                    try:
                        obj = getattr(mod, nm, None)
                        if inspect.isclass(obj):
                            comp_names.append(nm)
                    except Exception:
                        continue
            else:
                # Fallback: scan submodules and collect classes exposed in this category namespace
                # 1) classes directly in the aggregator module
                try:
                    for name, obj in inspect.getmembers(mod, inspect.isclass):
                        if obj.__module__.startswith(fq_module) and name[0].isupper():
                            comp_names.append(name)
                except Exception:
                    pass
                # 2) classes from submodules
                try:
                    if hasattr(mod, '__path__'):
                        # type: ignore[attr-defined]
                        for subinfo in pkgutil.walk_packages(mod.__path__, prefix=fq_module + '.'):
                            try:
                                smod = importlib.import_module(subinfo.name)
                                for name, obj in inspect.getmembers(smod, inspect.isclass):
                                    if obj.__module__.startswith(fq_module) and name[0].isupper():
                                        comp_names.append(name)
                            except Exception:
                                continue
                except Exception:
                    pass

            # Deduplicate and sort
            comp_names = sorted(sorted(set(comp_names)), key=str.lower)
            components[category] = comp_names
        return components

    def _build_aliases(self) -> Dict[str, str]:
        '''Build aliases dictionary by analyzing available components'''
        aliases: Dict[str, str] = {}

        def norm(s: str) -> str:
            return re.sub(r'[^a-z0-9]+', '', s.lower())

        for category, comps in self._components_by_category.items():
            for cls_name in comps:
                fqn = f'diagrams.aws.{category}.{cls_name}'
                # Primary aliases
                alias_keys = set()
                alias_keys.add(norm(cls_name))
                alias_keys.add(norm(f'{category}{cls_name}'))
                alias_keys.add(norm(f'{category}.{cls_name}'))
                alias_keys.add(norm(f'{category}-{cls_name}'))
                # Also add the exact class name lower as a convenience
                alias_keys.add(cls_name.lower())
                # Add AWS-like name e.g. EC2 -> ec2, S3 -> s3 already covered by norm, but keep
                for k in alias_keys:
                    aliases.setdefault(k, fqn)
        return aliases

    def get_node(self, node_type: str) -> Any:
        '''Get AWS component class using dynamic discovery with caching'''
        if not node_type or not isinstance(node_type, str):
            raise KeyError('node_type must be a non-empty string')

        with self._lock:
            # Cache by the exact user-provided key
            if node_type in self._class_cache:
                return self._class_cache[node_type]

            # Try direct import when a fully qualified path is provided
            if '.' in node_type:
                try:
                    module_path, _, class_name = node_type.rpartition('.')
                    if module_path and class_name:
                        mod = importlib.import_module(module_path)
                        cls = getattr(mod, class_name)
                        if inspect.isclass(cls):
                            self._class_cache[node_type] = cls
                            return cls
                except Exception:
                    pass

            # Try via aliases
            key = re.sub(r'[^a-z0-9]+', '', node_type.lower())
            fqn = self._aliases.get(key)
            if fqn:
                try:
                    module_path, _, class_name = fqn.rpartition('.')
                    mod = importlib.import_module(module_path)
                    cls = getattr(mod, class_name)
                    if inspect.isclass(cls):
                        # Cache under both the alias and requested node_type for faster future lookups
                        self._class_cache[node_type] = cls
                        self._class_cache[key] = cls
                        return cls
                except Exception:
                    pass

            # Not found
            raise KeyError(f'Unknown AWS node type: {node_type}')

    def list_available_components(self, category: str = None) -> Dict[str, List[str]]:
        '''List all available AWS components and their aliases'''
        if category is None:
            return {k: list(v) for k, v in self._components_by_category.items()}
        return {category: list(self._components_by_category.get(category, []))}
