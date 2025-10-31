
from typing import Dict, Any, Optional, Tuple


class EventDataNormalizer:

    @staticmethod
    def normalize_event_data(event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        '''标准化事件数据格式'''
        normalized = {}
        # Standardize user_id
        user_id = (
            event_data.get('user_id') or
            event_data.get('uid') or
            event_data.get('userId') or
            event_data.get('userid')
        )
        normalized['user_id'] = user_id

        # Standardize target_id
        target_id = (
            event_data.get('target_id') or
            event_data.get('tid') or
            event_data.get('targetId') or
            event_data.get('targetid')
        )
        normalized['target_id'] = target_id

        # Standardize is_group
        is_group = (
            event_data.get('is_group') or
            event_data.get('isGroup') or
            event_data.get('group', False)
        )
        if isinstance(is_group, str):
            is_group = is_group.lower() in ('true', '1', 'yes')
        normalized['is_group'] = bool(is_group)

        # Add event_type
        normalized['event_type'] = event_type

        # Optionally, add timestamp if present
        timestamp = (
            event_data.get('timestamp') or
            event_data.get('time') or
            event_data.get('ts')
        )
        if timestamp is not None:
            normalized['timestamp'] = timestamp

        # Add original data for reference
        normalized['original_data'] = event_data

        return normalized

    @staticmethod
    def extract_user_id(event_data: Dict[str, Any]) -> Optional[str]:
        '''从事件数据中提取用户ID'''
        return (
            event_data.get('user_id') or
            event_data.get('uid') or
            event_data.get('userId') or
            event_data.get('userid')
        )

    @staticmethod
    def extract_target_info(event_data: Dict[str, Any]) -> Tuple[Optional[str], bool]:
        target_id = (
            event_data.get('target_id') or
            event_data.get('tid') or
            event_data.get('targetId') or
            event_data.get('targetid')
        )
        is_group = (
            event_data.get('is_group') or
            event_data.get('isGroup') or
            event_data.get('group', False)
        )
        if isinstance(is_group, str):
            is_group = is_group.lower() in ('true', '1', 'yes')
        return target_id, bool(is_group)
