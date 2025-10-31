
from typing import List, Dict, Any
import importlib
import pkgutil


class AWSComponentRegistry:
    '''
    Class responsible for discovering and managing AWS components from the diagrams package.
    Encapsulates the component discovery, caching and lookup functionality.
    '''

    def __init__(self):
        self.categories = self._discover_categories()
        self.components = self._discover_components()
        self.aliases = self._build_aliases()

    def _discover_categories(self) -> List[str]:
        package = importlib.import_module('diagrams.aws')
        return [name for _, name, _ in pkgutil.iter_modules(package.__path__)]

    def _discover_components(self) -> Dict[str, List[str]]:
        components = {}
        for category in self.categories:
            package = importlib.import_module(f'diagrams.aws.{category}')
            components[category] = [name for name,
                                    obj in package.__dict__.items() if isinstance(obj, type)]
        return components

    def _build_aliases(self) -> Dict[str, str]:
        aliases = {}
        for category, component_list in self.components.items():
            for component in component_list:
                aliases[component.lower(
                )] = f'diagrams.aws.{category}.{component}'
        return aliases

    def get_node(self, node_type: str) -> Any:
        node_type = node_type.lower()
        if node_type in self.aliases:
            module_path = self.aliases[node_type]
            module = importlib.import_module(module_path.rsplit('.', 1)[0])
            return getattr(module, module_path.rsplit('.', 1)[1])
        raise ValueError(f"Node type {node_type} not found")

    def list_available_components(self, category: str = None) -> Dict[str, List[str]]:
        if category:
            if category in self.components:
                return {category: self.components[category]}
            else:
                raise ValueError(f"Category {category} not found")
        return self.components
