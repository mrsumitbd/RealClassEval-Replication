
from typing import Dict, Any, Optional, Tuple


class EventDataNormalizer:

    @staticmethod
    def normalize_event_data(event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        normalized_data = {'event_type': event_type}
        normalized_data.update(event_data)
        return normalized_data

    @staticmethod
    def extract_user_id(event_data: Dict[str, Any]) -> Optional[str]:
        return event_data.get('user_id') or event_data.get('uid')

    @staticmethod
    def extract_target_info(event_data: Dict[str, Any]) -> Tuple[Optional[str], bool]:
        target_id = event_data.get('target_id')
        is_anonymous = event_data.get('is_anonymous', False)
        return target_id, is_anonymous
