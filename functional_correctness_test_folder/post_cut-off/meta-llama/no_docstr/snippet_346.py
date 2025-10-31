
from typing import Dict, Any, Optional, Tuple


class EventDataNormalizer:

    @staticmethod
    def normalize_event_data(event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        normalized_data = event_data.copy()
        user_id = EventDataNormalizer.extract_user_id(event_data)
        target_id, is_target_internal = EventDataNormalizer.extract_target_info(
            event_data)

        normalized_data['event_type'] = event_type
        if user_id is not None:
            normalized_data['user_id'] = user_id
        if target_id is not None:
            normalized_data['target_id'] = target_id
        normalized_data['is_target_internal'] = is_target_internal

        return normalized_data

    @staticmethod
    def extract_user_id(event_data: Dict[str, Any]) -> Optional[str]:
        user_id = event_data.get('user_id') or event_data.get(
            'actor_id') or event_data.get('initiator_id')
        return user_id

    @staticmethod
    def extract_target_info(event_data: Dict[str, Any]) -> Tuple[Optional[str], bool]:
        target_id = event_data.get('target_id') or event_data.get(
            'resource_id') or event_data.get('object_id')
        is_target_internal = event_data.get(
            'is_internal_target', False) or event_data.get('is_target_internal', False)

        return target_id, is_target_internal
