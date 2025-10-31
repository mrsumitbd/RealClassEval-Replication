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

        action_type = action_type.strip().lower()
        allowed_types = {"end", "goto", "retry"}
        if action_type not in allowed_types:
            raise ValueError(
                f"action_type must be one of {sorted(allowed_types)}.")

        # Base action structure
        action: Dict[str, Any] = {"type": action_type, "name": name}

        # Validate and normalize per action type
        if action_type == "end":
            # Optional status; default to "success" if not provided
            status = action_definition.get("status", "success")
            if not isinstance(status, str) or status.strip() == "":
                raise ValueError(
                    "For 'end' action, 'status' must be a non-empty string if provided.")
            action["status"] = status
        elif action_type == "goto":
            # Require a target step identifier
            target = action_definition.get(
                "step", action_definition.get("target"))
            if not isinstance(target, str) or target.strip() == "":
                raise ValueError(
                    "For 'goto' action, 'step' (or 'target') must be a non-empty string.")
            action["step"] = target
        elif action_type == "retry":
            # Common retry controls (all optional but validate if present)
            retry_keys = ("maxAttempts", "delay",
                          "backoff", "jitter", "condition")
            for key in retry_keys:
                if key in action_definition:
                    action[key] = action_definition[key]

            if "maxAttempts" in action:
                if not isinstance(action["maxAttempts"], int) or action["maxAttempts"] < 1:
                    raise ValueError(
                        "For 'retry' action, 'maxAttempts' must be an integer >= 1.")
            if "delay" in action:
                if not isinstance(action["delay"], (int, float)) or action["delay"] < 0:
                    raise ValueError(
                        "For 'retry' action, 'delay' must be a non-negative number.")
            if "backoff" in action:
                if action["backoff"] not in ("constant", "linear", "exponential"):
                    raise ValueError(
                        "For 'retry' action, 'backoff' must be one of: 'constant', 'linear', 'exponential'.")
            if "jitter" in action:
                if not isinstance(action["jitter"], (bool, int, float)):
                    raise ValueError(
                        "For 'retry' action, 'jitter' must be a boolean or a number.")
                if isinstance(action["jitter"], (int, float)) and action["jitter"] < 0:
                    raise ValueError(
                        "For 'retry' action, numeric 'jitter' must be non-negative.")

        # Merge any additional, non-conflicting properties from action_definition
        for k, v in action_definition.items():
            if k not in action:
                action[k] = v

        return action

    @staticmethod
    def build_default_components() -> Dict[str, Any]:
        '''Build the default components section for an Arazzo specification.
        Returns:
            A dictionary containing the components section.
        '''
        components = {
            "schemas": {},
            "parameters": {},
            "constants": {},
            "actions": {},
            "errors": {},
            "messages": {},
            "workflows": {},
        }
        return {"components": components}
