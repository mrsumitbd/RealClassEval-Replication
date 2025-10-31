
from __future__ import annotations

from typing import Any, Dict, List


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
        # The Arazzo schema expects an action to contain at least the
        # following keys: `type`, `name`, and any additional properties.
        # We merge the supplied definition into the base dictionary.
        action: Dict[str, Any] = {
            "type": action_type,
            "name": name,
        }
        action.update(action_definition)
        return action

    @staticmethod
    def build_default_components() -> Dict[str, Any]:
        """
        Build the default components section for an Arazzo specification.

        Returns:
            A dictionary containing the components section.
        """
        # Default actions: success and failure. These are the minimal
        # required actions for a workflow to terminate.
        success_action = ArazzoComponentsBuilder.create_action(
            action_type="end",
            name="success",
            action_definition={"status": "success"},
        )
        failure_action = ArazzoComponentsBuilder.create_action(
            action_type="end",
            name="failure",
            action_definition={"status": "failure"},
        )

        # The components section may also contain conditions, variables,
        # and transitions. For a minimal default we provide empty lists.
        components: Dict[str, Any] = {
            "actions": [success_action, failure_action],
            "conditions": [],
            "variables": [],
            "transitions": [],
        }
        return components
