
from typing import Dict, Any, Optional, Tuple


class EventDataNormalizer:
    '''事件数据标准化器'''
    @staticmethod
    def normalize_event_data(event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        '''标准化事件数据格式'''
        normalized_data = {
            "type": event_type,
            "data": event_data
        }
        return normalized_data

    @staticmethod
    def extract_user_id(event_data: Dict[str, Any]) -> Optional[str]:
        '''从事件数据中提取用户ID'''
        return event_data.get("user_id")

    @staticmethod
    def extract_target_info(event_data: Dict[str, Any]) -> Tuple[Optional[str], bool]:
        '''从事件数据中提取目标信息，返回(target_id, is_group)'''
        target_id = event_data.get("target_id")
        is_group = event_data.get("is_group", False)
        return (target_id, is_group)
