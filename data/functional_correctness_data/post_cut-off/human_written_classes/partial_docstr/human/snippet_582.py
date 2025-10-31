from typing import Optional, Dict, Any, List

class BotpyEventAdapter:
    """Botpy事件适配器，将botpy事件转换为现有框架事件格式"""

    def __init__(self, event_handler):
        self.event_handler = event_handler

    def convert_message_to_event_data(self, message) -> Dict[str, Any]:
        """将botpy消息对象转换为现有框架的事件数据格式"""
        if isinstance(message, Message):
            return {'id': message.id, 'content': message.content, 'channel_id': message.channel_id, 'guild_id': message.guild_id, 'author': {'id': message.author.id, 'username': message.author.username, 'avatar': message.author.avatar, 'bot': message.author.bot}, 'timestamp': message.timestamp, 'type': 'AT_MESSAGE_CREATE'}
        elif isinstance(message, DirectMessage):
            return {'id': message.id, 'content': message.content, 'channel_id': message.channel_id, 'guild_id': message.guild_id, 'author': {'id': message.author.id, 'username': message.author.username, 'avatar': message.author.avatar}, 'timestamp': message.timestamp, 'type': 'DIRECT_MESSAGE_CREATE'}
        elif isinstance(message, GroupMessage):
            return {'id': message.id, 'content': message.content, 'group_openid': message.group_openid, 'author': {'member_openid': message.author.member_openid}, 'timestamp': message.timestamp, 'type': 'GROUP_AT_MESSAGE_CREATE'}
        elif isinstance(message, C2CMessage):
            return {'id': message.id, 'content': message.content, 'author': {'user_openid': message.author.user_openid}, 'timestamp': message.timestamp, 'type': 'C2C_MESSAGE_CREATE'}
        else:
            logger.warning(f'未知的消息类型: {type(message)}')
            return {}