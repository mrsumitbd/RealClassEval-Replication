
from typing import Any, Dict, Optional, Tuple


class EventDataNormalizer:
    """
    Normalizes event data dictionaries by extracting common fields such as user ID
    and target information. The implementation is intentionally generic to work
    with a variety of event payload shapes.
    """

    @staticmethod
    def normalize_event_data(event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalizes the raw event data into a flat dictionary containing:
            - event_type: the type of the event
            - user_id: the ID of the user who triggered the event (if any)
            - target_id: the ID of the target entity (if any)
            - is_target_user: True if the target is a user, False otherwise
            - original: the original event data (kept for reference)
        """
        user_id = EventDataNormalizer.extract_user_id(event_data)
        target_id, is_target_user = EventDataNormalizer.extract_target_info(
            event_data)

        normalized: Dict[str, Any] = {
            "event_type": event_type,
            "user_id": user_id,
            "target_id": target_id,
            "is_target_user": is_target_user,
            "original": event_data,
        }
        return normalized

    @staticmethod
    def extract_user_id(event_data: Dict[str, Any]) -> Optional[str]:
        """
        Attempts to extract a user ID from the event data. It checks common keys
        and nested structures. Returns None if no user ID is found.
        """
        # Direct keys
        for key in ("user_id", "userId", "uid", "user"):
            if key in event_data:
                val = event_data[key]
                if isinstance(val, str):
                    return val
                if isinstance(val, dict) and "id" in val:
                    return str(val["id"])

        # Nested under 'user' dict
        user = event_data.get("user")
        if isinstance(user, dict):
            for key in ("id", "user_id", "userId", "uid"):
                if key in user:
                    val = user[key]
                    if isinstance(val, str):
                        return val
                    if isinstance(val, (int, float)):
                        return str(val)

        # Fallback: look for any string that looks like an ID
        for key, val in event_data.items():
            if isinstance(val, str) and val.isdigit():
                return val

        return None

    @staticmethod
    def extract_target_info(event_data: Dict[str, Any]) -> Tuple[Optional[str], bool]:
        """
        Extracts target information from the event data. Returns a tuple:
            (target_id, is_target_user)
        where target_id is a string ID or None, and is_target_user indicates
        whether the target is a user entity.
        """
        target_id: Optional[str] = None
        is_user: bool = False

        # Common target keys
        for key in ("target_id", "targetId", "target"):
            if key in event_data:
                val = event_data[key]
                if isinstance(val, str):
                    target_id = val
                    # Heuristic: if key contains 'user' or value looks like a user ID
                    if "user" in key.lower():
                        is_user = True
                    break
                if isinstance(val, dict):
                    # Nested target dict
                    if "id" in val:
                        target_id = str(val["id"])
                    if "type" in val and isinstance(val["type"], str):
                        is_user = val["type"].lower() == "user"
                    break

        # If not found, try nested under 'target' dict
        if target_id is None:
            target = event_data.get("target")
            if isinstance(target, dict):
                if "id" in target:
                    target_id = str(target["id"])
                if "type" in target and isinstance(target["type"], str):
                    is_user = target["type"].lower() == "user"

        # Final fallback: any numeric string in the payload
        if target_id is None:
            for key, val in event_data.items():
                if isinstance(val, str) and val.isdigit():
                    target_id = val
                    break

        return target_id, is_user
