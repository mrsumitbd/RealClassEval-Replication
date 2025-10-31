
from typing import Dict, Any, Optional, Tuple


class EventDataNormalizer:

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
        '''提取目标信息和是否成功'''
        target_id = event_data.get("target_id")
        success = event_data.get("success", False)
        return target_id, success
