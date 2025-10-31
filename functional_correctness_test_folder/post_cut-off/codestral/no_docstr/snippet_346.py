
from typing import Dict, Any, Optional


class EventDataNormalizer:

    @staticmethod
    def normalize_event_data(event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        normalized_data = event_data.copy()
        if event_type == "click":
            normalized_data["action"] = "click"
        elif event_type == "purchase":
            normalized_data["action"] = "purchase"
            normalized_data["amount"] = normalized_data.get("amount", 0)
        elif event_type == "view":
            normalized_data["action"] = "view"
        return normalized_data

    @staticmethod
    def extract_user_id(event_data: Dict[str, Any]) -> Optional[str]:
        return event_data.get("user_id")

    @staticmethod
    def extract_target_info(event_data: Dict[str, Any]) -> tuple[Optional[str], bool]:
        target_id = event_data.get("target_id")
        is_success = event_data.get("is_success", False)
        return target_id, is_success
