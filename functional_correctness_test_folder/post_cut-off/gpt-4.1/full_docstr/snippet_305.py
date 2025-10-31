
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
        if action_type not in {'end', 'goto', 'retry'}:
            raise ValueError(f"Invalid action_type: {action_type}")
        action = {
            "type": action_type,
            "name": name
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
                    "type": "end",
                    "description": "Ends the workflow."
                },
                "goto": {
                    "type": "goto",
                    "description": "Jumps to another step."
                },
                "retry": {
                    "type": "retry",
                    "description": "Retries the current step."
                }
            }
        }
