from typing import Dict, Any, Optional, Union

class EventDataNormalizer:
    """事件数据标准化器"""

    @staticmethod
    def normalize_event_data(event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """标准化事件数据格式"""
        normalized = event_data.copy()
        normalized['type'] = event_type
        if 'author' in normalized:
            author = normalized['author']
            if isinstance(author, dict):
                user_id = author.get('id') or author.get('user_openid') or author.get('member_openid') or author.get('openid')
                if user_id and 'id' not in author:
                    author['id'] = user_id
        if 'timestamp' in normalized and normalized['timestamp']:
            pass
        return normalized

    @staticmethod
    def extract_user_id(event_data: Dict[str, Any]) -> Optional[str]:
        """从事件数据中提取用户ID"""
        author = event_data.get('author', {})
        user_id = author.get('id')
        if not user_id:
            user_id = author.get('openid')
        if not user_id:
            user_id = author.get('user_openid')
        if not user_id:
            user_id = author.get('member_openid')
        if not user_id:
            user_id = event_data.get('user', {}).get('openid')
        if not user_id:
            user_id = event_data.get('openid')
        return user_id

    @staticmethod
    def extract_target_info(event_data: Dict[str, Any]) -> tuple[Optional[str], bool]:
        """从事件数据中提取目标信息，返回(target_id, is_group)"""
        if 'group_openid' in event_data:
            return (event_data['group_openid'], True)
        if 'channel_id' in event_data:
            return (event_data['channel_id'], False)
        user_id = EventDataNormalizer.extract_user_id(event_data)
        if user_id:
            return (user_id, False)
        return (None, False)