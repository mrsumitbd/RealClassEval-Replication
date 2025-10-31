from typing import Any, Dict, Optional, Tuple


class EventDataNormalizer:
    '''事件数据标准化器'''

    @staticmethod
    def normalize_event_data(event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        '''标准化事件数据格式'''
        normalized = dict(event_data)
        # 标准化 user_id 字段
        if 'user_id' not in normalized:
            for key in ('userId', 'uid', 'from_user', 'fromUser', 'sender_id', 'senderId'):
                if key in normalized:
                    normalized['user_id'] = normalized[key]
                    break
        # 标准化 target_id 和 is_group 字段
        if 'target_id' not in normalized or 'is_group' not in normalized:
            for key in ('group_id', 'groupId', 'gid'):
                if key in normalized:
                    normalized['target_id'] = normalized[key]
                    normalized['is_group'] = True
                    break
            else:
                for key in ('user_id', 'userId', 'uid', 'to_user', 'toUser', 'target_user_id', 'targetUserId'):
                    if key in normalized and (key != 'user_id' or 'target_id' not in normalized):
                        normalized['target_id'] = normalized[key]
                        normalized['is_group'] = False
                        break
        # 标准化 event_type 字段
        normalized['event_type'] = event_type
        return normalized

    @staticmethod
    def extract_user_id(event_data: Dict[str, Any]) -> Optional[str]:
        '''从事件数据中提取用户ID'''
        for key in ('user_id', 'userId', 'uid', 'from_user', 'fromUser', 'sender_id', 'senderId'):
            if key in event_data:
                return str(event_data[key])
        return None

    @staticmethod
    def extract_target_info(event_data: Dict[str, Any]) -> Tuple[Optional[str], bool]:
        '''从事件数据中提取目标信息，返回(target_id, is_group)'''
        for key in ('group_id', 'groupId', 'gid'):
            if key in event_data:
                return str(event_data[key]), True
        for key in ('target_id', 'targetId', 'to_user', 'toUser', 'target_user_id', 'targetUserId', 'user_id', 'userId', 'uid'):
            if key in event_data:
                return str(event_data[key]), False
        return None, False
