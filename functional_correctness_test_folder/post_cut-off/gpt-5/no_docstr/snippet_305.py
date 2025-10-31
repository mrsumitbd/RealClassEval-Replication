from typing import Any, Dict
from copy import deepcopy


class ArazzoComponentsBuilder:
    @staticmethod
    def create_action(action_type: str, name: str, action_definition: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(action_type, str) or not action_type.strip():
            raise ValueError("action_type must be a non-empty string.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string.")
        if not isinstance(action_definition, dict):
            raise TypeError("action_definition must be a dict.")

        definition = deepcopy(action_definition)

        if "type" in definition and definition["type"] != action_type:
            raise ValueError(
                "action_definition['type'] conflicts with provided action_type.")
        if "name" in definition and definition["name"] != name:
            raise ValueError(
                "action_definition['name'] conflicts with provided name.")

        # Build action ensuring reserved keys are set correctly
        action: Dict[str, Any] = {
            "type": action_type,
            "name": name,
        }

        # Do not allow overriding reserved keys
        for k in ("type", "name"):
            definition.pop(k, None)

        action.update(definition)
        return action

    @staticmethod
    def build_default_components() -> Dict[str, Any]:
        return {
            "actions": {},
            "triggers": {},
            "connections": {},
            "metadata": {},
        }
