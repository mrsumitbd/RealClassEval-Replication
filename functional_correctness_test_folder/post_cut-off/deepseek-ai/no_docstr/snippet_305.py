
from typing import Any, Dict


class ArazzoComponentsBuilder:

    @staticmethod
    def create_action(action_type: str, name: str, action_definition: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "type": action_type,
            "name": name,
            "definition": action_definition
        }

    @staticmethod
    def build_default_components() -> Dict[str, Any]:
        return {
            "actions": [],
            "states": [],
            "transitions": []
        }
