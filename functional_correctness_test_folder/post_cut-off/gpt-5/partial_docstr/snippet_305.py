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
        if not isinstance(action_type, str) or action_type.strip() == "":
            raise ValueError("action_type must be a non-empty string.")
        if not isinstance(name, str) or name.strip() == "":
            raise ValueError("name must be a non-empty string.")
        if action_definition is None:
            action_definition = {}
        if not isinstance(action_definition, dict):
            raise TypeError("action_definition must be a dictionary.")

        allowed_types = {"end", "goto", "retry"}
        if action_type not in allowed_types:
            raise ValueError(
                f"Unsupported action_type '{action_type}'. Supported types: {sorted(allowed_types)}")

        action: Dict[str, Any] = {"type": action_type, "name": name}

        if action_type == "goto":
            step = action_definition.get("step")
            if not isinstance(step, str) or not step.strip():
                raise ValueError(
                    "For 'goto' actions, action_definition must include a non-empty 'step' string.")
            action["step"] = step

        elif action_type == "retry":
            max_retries = action_definition.get("maxRetries", 3)
            if not isinstance(max_retries, int) or max_retries < 1:
                raise ValueError(
                    "For 'retry' actions, 'maxRetries' must be a positive integer.")
            action["maxRetries"] = max_retries
            # Optional retry strategy fields
            if "strategy" in action_definition:
                if action_definition["strategy"] not in {"exponential", "linear", "fixed"}:
                    raise ValueError(
                        "If provided, 'strategy' must be one of: 'exponential', 'linear', 'fixed'.")
                action["strategy"] = action_definition["strategy"]
            if "delay" in action_definition:
                delay = action_definition["delay"]
                if not (isinstance(delay, (int, float)) and delay >= 0):
                    raise ValueError(
                        "If provided, 'delay' must be a non-negative number (seconds).")
                action["delay"] = delay
            if "maxDelay" in action_definition:
                max_delay = action_definition["maxDelay"]
                if not (isinstance(max_delay, (int, float)) and max_delay >= 0):
                    raise ValueError(
                        "If provided, 'maxDelay' must be a non-negative number (seconds).")
                action["maxDelay"] = max_delay

        # Merge any additional properties that don't conflict with validated keys
        protected_keys = set(action.keys())
        for k, v in action_definition.items():
            if k not in protected_keys:
                action[k] = v

        return action

    @staticmethod
    def build_default_components() -> Dict[str, Any]:
        '''Build the default components section for an Arazzo specification.
        Returns:
            A dictionary containing the components section.
        '''
        return {
            "schemas": {},
            "errors": {},
            "parameters": {},
            "variables": {},
            "messages": {},
            "securitySchemes": {},
        }
