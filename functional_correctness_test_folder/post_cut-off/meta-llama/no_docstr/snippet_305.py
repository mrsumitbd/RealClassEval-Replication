
from typing import Any, Dict


class ArazzoComponentsBuilder:

    @staticmethod
    def create_action(action_type: str, name: str, action_definition: Dict[str, Any]) -> Dict[str, Any]:
        """Creates an action component based on the given action type and definition."""
        action = {
            "type": action_type,
            "name": name,
        }
        action.update(action_definition)
        return action

    @staticmethod
    def build_default_components() -> Dict[str, Any]:
        """Builds default components for an Arazzo document."""
        return {
            "actions": {},
            "dependencies": {},
            "inputs": {},
            "outputs": {},
            "parameters": {},
            "securitySchemes": {},
            "servers": {},
        }
