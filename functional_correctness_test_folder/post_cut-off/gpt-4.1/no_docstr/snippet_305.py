
from typing import Any, Dict


class ArazzoComponentsBuilder:

    @staticmethod
    def create_action(action_type: str, name: str, action_definition: dict[str, Any]) -> dict[str, Any]:
        return {
            "type": action_type,
            "name": name,
            "definition": action_definition.copy() if action_definition else {}
        }

    @staticmethod
    def build_default_components() -> dict[str, Any]:
        return {
            "actions": [
                ArazzoComponentsBuilder.create_action(
                    "notify",
                    "default_notify",
                    {"message": "Default notification", "level": "info"}
                ),
                ArazzoComponentsBuilder.create_action(
                    "log",
                    "default_log",
                    {"message": "Default log entry", "level": "debug"}
                )
            ],
            "settings": {
                "retry": 3,
                "timeout": 30
            }
        }
