from typing import Any, Dict, Optional, Tuple


class EventDataNormalizer:
    '''事件数据标准化器'''

    @staticmethod
    def normalize_event_data(event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        '''标准化事件数据格式'''
        normalized = dict(event_data)
        # Normalize user_id
        if 'user_id' not in normalized:
            if 'uid' in normalized:
                normalized['user_id'] = normalized['uid']
            elif 'user' in normalized and isinstance(normalized['user'], dict):
                normalized['user_id'] = normalized['user'].get('id')
        # Normalize target_id and is_group
        if 'target_id' not in normalized or 'is_group' not in normalized:
            target_id, is_group = EventDataNormalizer.extract_target_info(
                normalized)
            normalized['target_id'] = target_id
            normalized['is_group'] = is_group
        # Optionally, add event_type if not present
        if 'event_type' not in normalized:
            normalized['event_type'] = event_type
        return normalized

    @staticmethod
    def extract_user_id(event_data: Dict[str, Any]) -> Optional[str]:
        '''从事件数据中提取用户ID'''
        if 'user_id' in event_data:
            return str(event_data['user_id'])
        if 'uid' in event_data:
            return str(event_data['uid'])
        if 'user' in event_data and isinstance(event_data['user'], dict):
            return str(event_data['user'].get('id')) if event_data['user'].get('id') is not None else None
        return None

    @staticmethod
    def extract_target_info(event_data: Dict[str, Any]) -> Tuple[Optional[str], bool]:
        '''从事件数据中提取目标信息，返回(target_id, is_group)'''
        # Group event
        if 'group_id' in event_data:
            return str(event_data['group_id']), True
        if 'gid' in event_data:
            return str(event_data['gid']), True
        if 'group' in event_data and isinstance(event_data['group'], dict):
            gid = event_data['group'].get('id')
            if gid is not None:
                return str(gid), True
        # Private event
        if 'user_id' in event_data:
            return str(event_data['user_id']), False
        if 'uid' in event_data:
            return str(event_data['uid']), False
        if 'user' in event_data and isinstance(event_data['user'], dict):
            uid = event_data['user'].get('id')
            if uid is not None:
                return str(uid), False
        return None, False
