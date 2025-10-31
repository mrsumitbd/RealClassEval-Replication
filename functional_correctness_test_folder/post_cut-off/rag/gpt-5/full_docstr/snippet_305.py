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
        if not isinstance(action_definition, dict):
            raise TypeError('action_definition must be a dict')

        if not isinstance(action_type, str) or not action_type.strip():
            raise ValueError('action_type must be a non-empty string')

        action_type_norm = action_type.strip().lower()
        allowed_types = {'end', 'goto', 'retry'}
        if action_type_norm not in allowed_types:
            raise ValueError(
                f'Unsupported action_type: {action_type}. Allowed: {sorted(allowed_types)}')

        if not isinstance(name, str) or not name.strip():
            raise ValueError('name must be a non-empty string')

        # Start building the action with mandatory fields.
        action: Dict[str, Any] = {
            'type': action_type_norm, 'name': name.strip()}

        # Prevent overriding required fields via action_definition.
        if 'type' in action_definition and action_definition['type'] != action_type_norm:
            raise ValueError(
                'action_definition must not override type to a different value')
        if 'name' in action_definition and str(action_definition['name']).strip() != name.strip():
            raise ValueError(
                'action_definition must not override name to a different value')

        # Merge remaining properties.
        for k, v in action_definition.items():
            if k not in ('type', 'name'):
                action[k] = v

        # Minimal validation for type-specific requirements.
        if action_type_norm == 'goto':
            step = action.get('step')
            if not isinstance(step, str) or not step.strip():
                raise ValueError(
                    "A 'goto' action must include a non-empty 'step' property")

        if action_type_norm == 'retry':
            # If present, validate recognized fields; at least one backoff/limit hint recommended.
            max_retries = action.get('maxRetries')
            if max_retries is not None:
                if not isinstance(max_retries, int) or max_retries < 0:
                    raise ValueError(
                        "'maxRetries' must be a non-negative integer when provided")

            after = action.get('after')
            if after is not None and not isinstance(after, str):
                raise ValueError(
                    "'after' must be an ISO 8601 duration string when provided")

            if max_retries is None and after is None and not any(k in action for k in ('when', 'exponentialBackoff', 'jitter')):
                # Ensure at least one retry-related hint exists.
                raise ValueError(
                    "A 'retry' action should include at least one of: 'maxRetries', 'after', 'when', 'exponentialBackoff', or 'jitter'")

        # 'end' requires no additional fields.

        return action

    @staticmethod
    def build_default_components() -> dict[str, Any]:
        '''Build the default components section for an Arazzo specification.
        Returns:
            A dictionary containing the components section.
        '''
        return {
            'schemas': {},
            'responses': {},
            'parameters': {},
            'examples': {},
            'requestBodies': {},
            'headers': {},
            'securitySchemes': {},
            'links': {},
            'callbacks': {},
            'pathItems': {},
        }
