
from typing import Dict, Any, Optional


class EventDataNormalizer:
    """事件数据标准化器"""

    @staticmethod
    def normalize_event_data(event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """标准化事件数据格式"""
        # Assuming some normalization logic here, this is a simple example
        normalized_data = {'event_type': event_type}
        normalized_data.update(event_data)
        return normalized_data

    @staticmethod
    def extract_user_id(event_data: Dict[str, Any]) -> Optional[str]:
        """从事件数据中提取用户ID"""
        # Assuming 'user_id' is a key in event_data
        return event_data.get('user_id')

    @staticmethod
    def extract_target_info(event_data: Dict[str, Any]) -> tuple[Optional[str], bool]:
        """从事件数据中提取目标信息，返回(target_id, is_group)"""
        # Assuming 'target_id' and 'is_group' are keys in event_data
        target_id = event_data.get('target_id')
        is_group = event_data.get('is_group', False)
        return target_id, is_group
