
class ArazzoComponentsBuilder:

    @staticmethod
    def create_action(action_type: str, name: str, action_definition: dict[str, Any]) -> dict[str, Any]:
        action = {
            "type": action_type,
            "name": name,
            "definition": action_definition
        }
        return action

    @staticmethod
    def build_default_components() -> dict[str, Any]:
        components = {
            "actions": [],
            "triggers": [],
            "conditions": []
        }
        return components
