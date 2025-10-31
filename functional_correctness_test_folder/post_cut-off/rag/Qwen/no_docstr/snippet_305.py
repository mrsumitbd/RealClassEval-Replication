
from typing import Any, Dict


class ArazzoComponentsBuilder:
    '''Builder for Arazzo components section.'''
    @staticmethod
    def create_action(action_type: str, name: str, action_definition: Dict[str, Any]) -> Dict[str, Any]:
        '''Create an action (success or failure) that complies with the Arazzo schema.
        Args:
            action_type: The type of action ('end', 'goto', or 'retry').
            name: The name of the action.
            action_definition: Additional properties for the action.
        Returns:
            A valid action object according to the Arazzo schema.
        '''
        if action_type not in ['end', 'goto', 'retry']:
            raise ValueError("action_type must be 'end', 'goto', or 'retry'")

        action = {
            "type": action_type,
            "name": name
        }
        action.update(action_definition)
        return action

    @staticmethod
    def build_default_components() -> Dict[str, Any]:
        '''Build the default components section for an Arazzo specification.
        Returns:
            A dictionary containing the components section.
        '''
        return {
            "components": {
                "actions": {
                    "success": ArazzoComponentsBuilder.create_action('end', 'success', {}),
                    "failure": ArazzoComponentsBuilder.create_action('retry', 'failure', {'max_retries': 3})
                },
                "triggers": {
                    "start": {
                        "type": "event",
                        "name": "start_event"
                    }
                }
            }
        }
