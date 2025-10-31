
from __future__ import annotations

from typing import Any, Dict


class ArazzoComponentsBuilder:
    """Builder for Arazzo components section."""

    @staticmethod
    def create_action(
        action_type: str,
        name: str,
        action_definition: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Create an action (success or failure) that complies with the Arazzo schema.

        Args:
            action_type: The type of action ('end', 'goto', or 'retry').
            name: The name of the action.
            action_definition: Additional properties for the action.

        Returns:
            A valid action object according to the Arazzo schema.
        """
        allowed_types = {"end", "goto", "retry"}
        if action_type not in allowed_types:
            raise ValueError(
                f"Unsupported action_type '{action_type}'. "
                f"Allowed types are: {', '.join(sorted(allowed_types))}"
            )

        # Build the action dictionary. The schema expects a 'name' and a 'type'
        # field, followed by any additional properties supplied in
        # `action_definition`.
        action: Dict[str, Any] = {"name": name, "type": action_type}
        action.update(action_definition)
        return action

    @staticmethod
    def build_default_components() -> Dict[str, Any]:
        """
        Build the default components section for an Arazzo specification.

        Returns:
            A dictionary containing the components section.
        """
        # The minimal components section contains empty dictionaries for
        # actions, states, and variables.  This can be extended by callers
        # as needed.
        return {"actions": {}, "states": {}, "variables": {}}
