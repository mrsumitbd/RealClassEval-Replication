from datetime import datetime
from src.chat.message_receive.message import MessageRecv

class ContextMessage:
    """上下文消息类"""

    def __init__(self, message: MessageRecv):
        self.user_name = message.message_info.user_info.user_nickname
        self.user_id = message.message_info.user_info.user_id
        self.content = message.processed_plain_text
        self.timestamp = datetime.now()
        self.group_name = message.message_info.group_info.group_name if message.message_info.group_info else '私聊'
        self.is_gift = getattr(message, 'is_gift', False)
        self.is_superchat = getattr(message, 'is_superchat', False)
        if self.is_gift:
            self.gift_name = getattr(message, 'gift_name', '')
            self.gift_count = getattr(message, 'gift_count', '1')
            self.content = f'送出了 {self.gift_name} x{self.gift_count}'
        elif self.is_superchat:
            self.superchat_price = getattr(message, 'superchat_price', '0')
            self.superchat_message = getattr(message, 'superchat_message_text', '')
            if self.superchat_message:
                self.content = f'[¥{self.superchat_price}] {self.superchat_message}'
            else:
                self.content = f'[¥{self.superchat_price}] {self.content}'

    def to_dict(self):
        return {'user_name': self.user_name, 'user_id': self.user_id, 'content': self.content, 'timestamp': self.timestamp.strftime('%m-%d %H:%M:%S'), 'group_name': self.group_name, 'is_gift': self.is_gift, 'is_superchat': self.is_superchat}