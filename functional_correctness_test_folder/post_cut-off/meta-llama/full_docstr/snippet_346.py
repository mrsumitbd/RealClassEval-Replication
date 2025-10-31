
from typing import Dict, Any, Optional


class EventDataNormalizer:
    '''事件数据标准化器'''
    @staticmethod
    def normalize_event_data(event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        '''标准化事件数据格式'''
        normalized_data = event_data.copy()
        if event_type == 'message':
            normalized_data['message_type'] = event_data.get(
                'message_type', 'private')
            if normalized_data['message_type'] == 'group':
                normalized_data['group_id'] = event_data.get('group_id')
            elif normalized_data['message_type'] == 'private':
                normalized_data['user_id'] = event_data.get('user_id')
        elif event_type == 'notice':
            normalized_data['notice_type'] = event_data.get('notice_type')
            if normalized_data['notice_type'] == 'group_decrease':
                normalized_data['sub_type'] = event_data.get('sub_type')
        return normalized_data

    @staticmethod
    def extract_user_id(event_data: Dict[str, Any]) -> Optional[str]:
        '''从事件数据中提取用户ID'''
        if 'user_id' in event_data:
            return str(event_data['user_id'])
        elif 'sender' in event_data and 'user_id' in event_data['sender']:
            return str(event_data['sender']['user_id'])
        return None

    @staticmethod
    def extract_target_info(event_data: Dict[str, Any]) -> tuple[Optional[str], bool]:
        '''从事件数据中提取目标信息，返回(target_id, is_group)'''
        if 'group_id' in event_data:
            return str(event_data['group_id']), True
        elif 'user_id' in event_data:
            return str(event_data['user_id']), False
        elif 'sender' in event_data and 'user_id' in event_data['sender']:
            return str(event_data['sender']['user_id']), False
        return None, False
