
from typing import Dict, Any, Optional, Tuple


class EventDataNormalizer:

    @staticmethod
    def normalize_event_data(event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        normalized_data = {
            'event_type': event_type,
            'user_id': EventDataNormalizer.extract_user_id(event_data),
            'target_info': EventDataNormalizer.extract_target_info(event_data)
        }
        return normalized_data

    @staticmethod
    def extract_user_id(event_data: Dict[str, Any]) -> Optional[str]:
        return event_data.get('user', {}).get('id')

    @staticmethod
    def extract_target_info(event_data: Dict[str, Any]) -> Tuple[Optional[str], bool]:
        target = event_data.get('target')
        target_id = target.get('id') if target else None
        is_active = target.get('is_active', False) if target else False
        return target_id, is_active
