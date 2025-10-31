import time
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class SuperChatRecord:
    """SuperChat记录数据类"""
    user_id: str
    user_nickname: str
    platform: str
    chat_id: str
    price: float
    message_text: str
    timestamp: float
    expire_time: float
    group_name: Optional[str] = None

    def is_expired(self) -> bool:
        """检查SuperChat是否已过期"""
        return time.time() > self.expire_time

    def remaining_time(self) -> float:
        """获取剩余时间（秒）"""
        return max(0, self.expire_time - time.time())

    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {'user_id': self.user_id, 'user_nickname': self.user_nickname, 'platform': self.platform, 'chat_id': self.chat_id, 'price': self.price, 'message_text': self.message_text, 'timestamp': self.timestamp, 'expire_time': self.expire_time, 'group_name': self.group_name, 'remaining_time': self.remaining_time()}