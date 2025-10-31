from typing import Any


class ArazzoComponentsBuilder:
    '''Builder for Arazzo components section.'''
    _ALLOWED_ACTION_TYPES = {'end', 'goto', 'retry'}

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
        if action_type not in ArazzoComponentsBuilder._ALLOWED_ACTION_TYPES:
            raise ValueError(
                f'Unsupported action_type: {action_type!r}. Expected one of {sorted(ArazzoComponentsBuilder._ALLOWED_ACTION_TYPES)}.')
        if not isinstance(name, str) or not name.strip():
            raise ValueError('name must be a non-empty string.')
        if action_definition is None:
            action_definition = {}
        if not isinstance(action_definition, dict):
            raise TypeError('action_definition must be a dictionary.')

        body: dict[str, Any] = {'name': name}
        # Merge additional properties; explicit name parameter takes precedence.
        for k, v in action_definition.items():
            if k == 'name':
                continue
            body[k] = v

        return {action_type: body}

    @staticmethod
    def build_default_components() -> dict[str, Any]:
        '''Build the default components section for an Arazzo specification.
        Returns:
            A dictionary containing the components section.
        '''
        success_action = ArazzoComponentsBuilder.create_action(
            'end', 'success', {})
        failure_action = ArazzoComponentsBuilder.create_action(
            'end', 'failure', {})

        return {
            'actions': {
                'success': [success_action],
                'failure': [failure_action],
            }
        }
