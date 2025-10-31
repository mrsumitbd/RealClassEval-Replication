
from typing import Dict, Any, Optional


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
            'timestamp': event_data.get('timestamp'),
            'additional_info': {}
        }

        target_id, is_group = EventDataNormalizer.extract_target_info(
            event_data)
        normalized_data['target_id'] = target_id
        normalized_data['is_group'] = is_group

        for key, value in event_data.items():
            if key not in ['user_id', 'target_id', 'is_group', 'timestamp']:
                normalized_data['additional_info'][key] = value

        return normalized_data

    @staticmethod
    def extract_user_id(event_data: Dict[str, Any]) -> Optional[str]:
        '''从事件数据中提取用户ID'''
        user_id = event_data.get('user_id')
        if user_id is None:
            user_id = event_data.get('user', {}).get('id')
        return user_id

    @staticmethod
    def extract_target_info(event_data: Dict[str, Any]) -> tuple[Optional[str], bool]:
        '''从事件数据中提取目标信息，返回(target_id, is_group)'''
        target_id = event_data.get('target_id')
        is_group = event_data.get('is_group', False)

        if target_id is None:
            target = event_data.get('target')
            if target is not None:
                target_id = target.get('id')
                is_group = target.get('is_group', False)

        return target_id, is_group
