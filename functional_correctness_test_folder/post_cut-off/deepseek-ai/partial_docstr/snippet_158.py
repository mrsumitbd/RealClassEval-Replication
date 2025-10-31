
from typing import List, Dict, Any
import diagrams.aws as aws
import inspect


class AWSComponentRegistry:
    '''
    Class responsible for discovering and managing AWS components from the diagrams package.
    Encapsulates the component discovery, caching and lookup functionality.
    '''

    def __init__(self):
        self._categories = self._discover_categories()
        self._components = self._discover_components()
        self._aliases = self._build_aliases()

    def _discover_categories(self) -> List[str]:
        categories = []
        for name, obj in inspect.getmembers(aws):
            if inspect.ismodule(obj) and not name.startswith('_'):
                categories.append(name)
        return categories

    def _discover_components(self) -> Dict[str, List[str]]:
        components = {}
        for category in self._categories:
            module = getattr(aws, category)
            component_list = []
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and not name.startswith('_'):
                    component_list.append(name)
            components[category] = component_list
        return components

    def _build_aliases(self) -> Dict[str, str]:
        aliases = {}
        for category, components in self._components.items():
            for component in components:
                aliases[component.lower()] = f"{category}.{component}"
        return aliases

    def get_node(self, node_type: str) -> Any:
        if node_type.lower() not in self._aliases:
            raise ValueError(f"Unknown node type: {node_type}")
        module_path, class_name = self._aliases[node_type.lower()].split('.')
        module = getattr(aws, module_path)
        return getattr(module, class_name)

    def list_available_components(self, category: str = None) -> Dict[str, List[str]]:
        if category is None:
            return self._components.copy()
        if category not in self._categories:
            raise ValueError(f"Unknown category: {category}")
        return {category: self._components[category]}
