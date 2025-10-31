
from typing import Dict, Any, Optional, Tuple


class EventDataNormalizer:

    @staticmethod
    def normalize_event_data(event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        '''标准化事件数据格式'''
        normalized_data = {
            'event_type': event_type,
            'user_id': EventDataNormalizer.extract_user_id(event_data),
            'target_id': EventDataNormalizer.extract_target_info(event_data)[0],
            'is_target_valid': EventDataNormalizer.extract_target_info(event_data)[1],
            'raw_data': event_data
        }
        return normalized_data

    @staticmethod
    def extract_user_id(event_data: Dict[str, Any]) -> Optional[str]:
        '''从事件数据中提取用户ID'''
        return event_data.get('user_id', None)

    @staticmethod
    def extract_target_info(event_data: Dict[str, Any]) -> Tuple[Optional[str], bool]:
        target_id = event_data.get('target_id', None)
        is_valid = target_id is not None and isinstance(target_id, str)
        return target_id, is_valid
