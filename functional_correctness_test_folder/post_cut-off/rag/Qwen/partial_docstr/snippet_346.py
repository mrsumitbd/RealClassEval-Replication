
from typing import Dict, Any, Optional, Tuple


class EventDataNormalizer:
    '''事件数据标准化器'''
    @staticmethod
    def normalize_event_data(event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        '''标准化事件数据格式'''
        normalized_data = {
            'event_type': event_type,
            'user_id': EventDataNormalizer.extract_user_id(event_data),
            'target_id': None,
            'is_group': False,
            'details': event_data
        }
        target_id, is_group = EventDataNormalizer.extract_target_info(
            event_data)
        normalized_data['target_id'] = target_id
        normalized_data['is_group'] = is_group
        return normalized_data

    @staticmethod
    def extract_user_id(event_data: Dict[str, Any]) -> Optional[str]:
        '''从事件数据中提取用户ID'''
        return event_data.get('user_id') or event_data.get('userId') or event_data.get('actor_id')

    @staticmethod
    def extract_target_info(event_data: Dict[str, Any]) -> Tuple[Optional[str], bool]:
        '''从事件数据中提取目标信息，返回(target_id, is_group)'''
        target_id = event_data.get('target_id') or event_data.get('targetId')
        is_group = event_data.get(
            'is_group', False) or event_data.get('isGroup', False)
        return target_id, is_group
