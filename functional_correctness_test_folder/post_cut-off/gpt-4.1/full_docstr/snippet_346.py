
from typing import Dict, Any, Optional


class EventDataNormalizer:
    '''事件数据标准化器'''

    @staticmethod
    def normalize_event_data(event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        '''标准化事件数据格式'''
        normalized = {}
        # 标准化用户ID
        user_id = EventDataNormalizer.extract_user_id(event_data)
        if user_id is not None:
            normalized['user_id'] = user_id
        # 标准化目标信息
        target_id, is_group = EventDataNormalizer.extract_target_info(
            event_data)
        if target_id is not None:
            normalized['target_id'] = target_id
            normalized['is_group'] = is_group
        # 标准化事件类型
        normalized['event_type'] = event_type
        # 标准化时间戳
        if 'timestamp' in event_data:
            normalized['timestamp'] = event_data['timestamp']
        elif 'time' in event_data:
            normalized['timestamp'] = event_data['time']
        # 其他常见字段
        for key in ['message', 'content', 'text']:
            if key in event_data:
                normalized['message'] = event_data[key]
                break
        return normalized

    @staticmethod
    def extract_user_id(event_data: Dict[str, Any]) -> Optional[str]:
        '''从事件数据中提取用户ID'''
        for key in ['user_id', 'uid', 'user', 'from_user', 'sender_id']:
            if key in event_data:
                val = event_data[key]
                if isinstance(val, dict):
                    # 可能嵌套
                    for subkey in ['id', 'user_id', 'uid']:
                        if subkey in val:
                            return str(val[subkey])
                else:
                    return str(val)
        return None

    @staticmethod
    def extract_target_info(event_data: Dict[str, Any]) -> tuple[Optional[str], bool]:
        '''从事件数据中提取目标信息，返回(target_id, is_group)'''
        # 群聊目标
        for group_key in ['group_id', 'gid', 'group', 'chat_id', 'room_id']:
            if group_key in event_data:
                val = event_data[group_key]
                if isinstance(val, dict):
                    for subkey in ['id', 'group_id', 'gid']:
                        if subkey in val:
                            return str(val[subkey]), True
                else:
                    return str(val), True
        # 私聊目标
        for user_key in ['to_user_id', 'target_user_id', 'to_uid', 'to_user', 'recipient_id']:
            if user_key in event_data:
                val = event_data[user_key]
                if isinstance(val, dict):
                    for subkey in ['id', 'user_id', 'uid']:
                        if subkey in val:
                            return str(val[subkey]), False
                else:
                    return str(val), False
        # 某些事件只有 user_id
        if 'user_id' in event_data:
            return str(event_data['user_id']), False
        return None, False
