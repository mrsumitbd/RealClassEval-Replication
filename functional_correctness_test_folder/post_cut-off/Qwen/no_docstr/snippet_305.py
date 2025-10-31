
from typing import Any, Dict


class ArazzoComponentsBuilder:

    @staticmethod
    def create_action(action_type: str, name: str, action_definition: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "action_type": action_type,
            "name": name,
            "definition": action_definition
        }

    @staticmethod
    def build_default_components() -> Dict[str, Any]:
        return {
            "actions": [
                ArazzoComponentsBuilder.create_action(
                    "click", "button_click", {"element": "button", "value": "submit"}),
                ArazzoComponentsBuilder.create_action("hover", "hover_over_image", {
                                                      "element": "image", "value": "logo"})
            ],
            "settings": {
                "theme": "light",
                "language": "en"
            }
        }
