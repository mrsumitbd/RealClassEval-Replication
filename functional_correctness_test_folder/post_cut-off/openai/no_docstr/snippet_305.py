
from typing import Any, Dict


class ArazzoComponentsBuilder:
    """
    Utility class for building action components and a set of default components.
    """

    @staticmethod
    def create_action(action_type: str, name: str, action_definition: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a single action component.

        Parameters
        ----------
        action_type : str
            The type of the action (e.g., "start", "task", "end").
        name : str
            The unique name of the action.
        action_definition : dict[str, Any]
            A dictionary containing the definition of the action.

        Returns
        -------
        dict[str, Any]
            A dictionary representing the action component.
        """
        if not isinstance(action_type, str) or not action_type:
            raise ValueError("action_type must be a non-empty string")
        if not isinstance(name, str) or not name:
            raise ValueError("name must be a non-empty string")
        if not isinstance(action_definition, dict):
            raise ValueError("action_definition must be a dictionary")

        return {
            "type": action_type,
            "name": name,
            "definition": action_definition,
        }

    @staticmethod
    def build_default_components() -> Dict[str, Any]:
        """
        Build a set of default components that can be used as a starting point.

        Returns
        -------
        dict[str, Any]
            A dictionary mapping component names to their definitions.
        """
        defaults: Dict[str, Any] = {}

        # Start component
        defaults["start"] = ArazzoComponentsBuilder.create_action(
            action_type="start",
            name="start",
            action_definition={
                "description": "Entry point of the workflow",
                "next": None,
            },
        )

        # Task component
        defaults["task"] = ArazzoComponentsBuilder.create_action(
            action_type="task",
            name="task",
            action_definition={
                "description": "Generic task placeholder",
                "next": None,
            },
        )

        # End component
        defaults["end"] = ArazzoComponentsBuilder.create_action(
            action_type="end",
            name="end",
            action_definition={
                "description": "Exit point of the workflow",
                "next": None,
            },
        )

        return defaults
