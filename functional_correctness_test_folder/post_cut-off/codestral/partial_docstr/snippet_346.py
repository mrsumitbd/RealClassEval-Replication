
from typing import Dict, Any, Optional, Tuple


class EventDataNormalizer:

    @staticmethod
    def normalize_event_data(event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        normalized_data = {
            'event_type': event_type,
            'timestamp': event_data.get('timestamp'),
            'user_id': EventDataNormalizer.extract_user_id(event_data),
            'target_id': EventDataNormalizer.extract_target_info(event_data)[0],
            'is_success': EventDataNormalizer.extract_target_info(event_data)[1]
        }
        return normalized_data

    @staticmethod
    def extract_user_id(event_data: Dict[str, Any]) -> Optional[str]:
        user_id = event_data.get('user_id')
        if user_id is not None:
            return str(user_id)
        return None

    @staticmethod
    def extract_target_info(event_data: Dict[str, Any]) -> Tuple[Optional[str], bool]:
        target_id = event_data.get('target_id')
        is_success = event_data.get('is_success', False)
        if target_id is not None:
            return str(target_id), bool(is_success)
        return None, bool(is_success)
