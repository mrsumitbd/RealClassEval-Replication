from typing import Dict, Optional, TYPE_CHECKING
import time
from maim_message import GroupInfo, UserInfo

class ChatStream:
    """聊天流对象，存储一个完整的聊天上下文"""

    def __init__(self, stream_id: str, platform: str, user_info: UserInfo, group_info: Optional[GroupInfo]=None, data: Optional[dict]=None):
        self.stream_id = stream_id
        self.platform = platform
        self.user_info = user_info
        self.group_info = group_info
        self.create_time = data.get('create_time', time.time()) if data else time.time()
        self.last_active_time = data.get('last_active_time', self.create_time) if data else self.create_time
        self.saved = False
        self.context: ChatMessageContext = None

    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {'stream_id': self.stream_id, 'platform': self.platform, 'user_info': self.user_info.to_dict() if self.user_info else None, 'group_info': self.group_info.to_dict() if self.group_info else None, 'create_time': self.create_time, 'last_active_time': self.last_active_time}

    @classmethod
    def from_dict(cls, data: dict) -> 'ChatStream':
        """从字典创建实例"""
        user_info = UserInfo.from_dict(data.get('user_info', {})) if data.get('user_info') else None
        group_info = GroupInfo.from_dict(data.get('group_info', {})) if data.get('group_info') else None
        return cls(stream_id=data['stream_id'], platform=data['platform'], user_info=user_info, group_info=group_info, data=data)

    def update_active_time(self):
        """更新最后活跃时间"""
        self.last_active_time = time.time()
        self.saved = False

    def set_context(self, message: 'MessageRecv'):
        """设置聊天消息上下文"""
        self.context = ChatMessageContext(message)