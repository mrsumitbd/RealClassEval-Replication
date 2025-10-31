from typing import Dict, Optional, TYPE_CHECKING

class ChatMessageContext:
    """聊天消息上下文，存储消息的上下文信息"""

    def __init__(self, message: 'MessageRecv'):
        self.message = message

    def get_template_name(self) -> Optional[str]:
        """获取模板名称"""
        if self.message.message_info.template_info and (not self.message.message_info.template_info.template_default):
            return self.message.message_info.template_info.template_name
        return None

    def get_last_message(self) -> 'MessageRecv':
        """获取最后一条消息"""
        return self.message

    def check_types(self, types: list) -> bool:
        """检查消息类型"""
        if not self.message.message_info.format_info.accept_format:
            return False
        for t in types:
            if t not in self.message.message_info.format_info.accept_format:
                return False
        return True

    def get_priority_mode(self) -> str:
        """获取优先级模式"""
        return self.message.priority_mode

    def get_priority_info(self) -> Optional[dict]:
        """获取优先级信息"""
        if hasattr(self.message, 'priority_info') and self.message.priority_info:
            return self.message.priority_info
        return None