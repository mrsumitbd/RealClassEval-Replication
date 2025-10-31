from typing import Any


class ArazzoComponentsBuilder:
    """Builder for Arazzo components section."""

    @staticmethod
    def create_action(action_type: str, name: str, action_definition: dict[str, Any]) -> dict[str, Any]:
        """Create an action (success or failure) that complies with the Arazzo schema.
        Args:
            action_type: The type of action ('end', 'goto', or 'retry').
            name: The name of the action.
            action_definition: Additional properties for the action.
        Returns:
            A valid action object according to the Arazzo schema.
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Action 'name' must be a non-empty string.")

        if action_definition is None:
            action_definition = {}
        if not isinstance(action_definition, dict):
            raise TypeError("action_definition must be a dictionary.")

        normalized_type = (action_type or "").strip().lower()
        allowed_types = {"end", "goto", "retry"}
        if normalized_type not in allowed_types:
            raise ValueError(
                f"Unsupported action_type '{action_type}'. Allowed: {sorted(allowed_types)}")

        if "name" in action_definition or "type" in action_definition:
            raise ValueError(
                "action_definition must not redefine reserved keys: 'name', 'type'.")

        # Best-effort light validation for known types without enforcing strict requirements.
        if normalized_type == "goto" and "step" in action_definition:
            if not isinstance(action_definition["step"], str) or not action_definition["step"].strip():
                raise ValueError(
                    "For 'goto' actions, 'step' must be a non-empty string if provided.")
        if normalized_type == "retry" and "maxAttempts" in action_definition:
            max_attempts = action_definition["maxAttempts"]
            if not isinstance(max_attempts, int) or max_attempts < 1:
                raise ValueError(
                    "'maxAttempts' must be an integer >= 1 when provided for 'retry'.")

        action: dict[str, Any] = {"name": name, "type": normalized_type}
        action.update(action_definition)
        return action

    @staticmethod
    def build_default_components() -> dict[str, Any]:
        """Build the default components section for an Arazzo specification.
        Returns:
            A dictionary containing the components section.
        """
        return {
            "schemas": {},
            "tools": {},
            "workflows": {},
            "steps": {},
            "errors": {},
        }
