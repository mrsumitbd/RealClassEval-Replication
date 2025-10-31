
from typing import Any, Dict


class ArazzoComponentsBuilder:
    '''Builder for Arazzo components section.'''
    @staticmethod
    def create_action(action_type: str, name: str, action_definition: dict[str, Any]) -> dict[str, Any]:
        '''Create an action (success or failure) that complies with the Arazzo schema.
        Args:
            action_type: The type of action ('end', 'goto', or 'retry').
            name: The name of the action.
            action_definition: Additional properties for the action.
        Returns:
            A valid action object according to the Arazzo schema.
        '''
        action = {
            "name": name,
            "type": action_type
        }
        if action_definition:
            action.update(action_definition)
        return action

    @staticmethod
    def build_default_components() -> dict[str, Any]:
        '''Build the default components section for an Arazzo specification.
        Returns:
            A dictionary containing the components section.
        '''
        return {
            "actions": {
                "end": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "type": {"type": "string", "enum": ["end"]},
                        "reason": {"type": "string"}
                    },
                    "required": ["name", "type"]
                },
                "goto": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "type": {"type": "string", "enum": ["goto"]},
                        "target": {"type": "string"}
                    },
                    "required": ["name", "type", "target"]
                },
                "retry": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "type": {"type": "string", "enum": ["retry"]},
                        "max_attempts": {"type": "integer"}
                    },
                    "required": ["name", "type"]
                }
            }
        }
