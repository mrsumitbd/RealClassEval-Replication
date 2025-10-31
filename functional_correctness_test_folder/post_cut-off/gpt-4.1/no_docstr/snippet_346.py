
from typing import Dict, Any, Optional, Tuple


class EventDataNormalizer:

    @staticmethod
    def normalize_event_data(event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        normalized = {}
        # Normalize user_id
        user_id = EventDataNormalizer.extract_user_id(event_data)
        if user_id is not None:
            normalized['user_id'] = user_id
        # Normalize target info
        target_id, is_group = EventDataNormalizer.extract_target_info(
            event_data)
        if target_id is not None:
            normalized['target_id'] = target_id
            normalized['is_group'] = is_group
        # Add event_type
        normalized['event_type'] = event_type
        # Optionally, add timestamp if present
        if 'timestamp' in event_data:
            normalized['timestamp'] = event_data['timestamp']
        elif 'time' in event_data:
            normalized['timestamp'] = event_data['time']
        return normalized

    @staticmethod
    def extract_user_id(event_data: Dict[str, Any]) -> Optional[str]:
        # Try common keys for user id
        for key in ['user_id', 'userid', 'user', 'uid']:
            if key in event_data and event_data[key] is not None:
                return str(event_data[key])
        # Sometimes user info is nested
        if 'user' in event_data and isinstance(event_data['user'], dict):
            for key in ['id', 'user_id', 'uid']:
                if key in event_data['user'] and event_data['user'][key] is not None:
                    return str(event_data['user'][key])
        return None

    @staticmethod
    def extract_target_info(event_data: Dict[str, Any]) -> Tuple[Optional[str], bool]:
        # Try to extract group or channel id
        for group_key in ['group_id', 'groupid', 'gid', 'channel_id', 'channelid', 'cid']:
            if group_key in event_data and event_data[group_key] is not None:
                return str(event_data[group_key]), True
        # Sometimes group info is nested
        if 'group' in event_data and isinstance(event_data['group'], dict):
            for key in ['id', 'group_id', 'gid']:
                if key in event_data['group'] and event_data['group'][key] is not None:
                    return str(event_data['group'][key]), True
        if 'channel' in event_data and isinstance(event_data['channel'], dict):
            for key in ['id', 'channel_id', 'cid']:
                if key in event_data['channel'] and event_data['channel'][key] is not None:
                    return str(event_data['channel'][key]), True
        # If not group, try to extract a direct target user
        for user_key in ['target_user_id', 'target_user', 'to_user_id', 'to_user', 'recipient_id']:
            if user_key in event_data and event_data[user_key] is not None:
                return str(event_data[user_key]), False
        # Sometimes target info is nested
        if 'target' in event_data and isinstance(event_data['target'], dict):
            for key in ['id', 'user_id', 'uid']:
                if key in event_data['target'] and event_data['target'][key] is not None:
                    return str(event_data['target'][key]), False
        return None, False
