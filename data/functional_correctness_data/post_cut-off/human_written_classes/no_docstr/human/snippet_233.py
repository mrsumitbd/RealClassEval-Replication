from src.chat.message_receive.chat_stream import ChatStream, get_chat_manager
from typing import Optional, Dict, Tuple, List

class S4UChatManager:

    def __init__(self):
        self.s4u_chats: Dict[str, 'S4UChat'] = {}

    def get_or_create_chat(self, chat_stream: ChatStream) -> 'S4UChat':
        if chat_stream.stream_id not in self.s4u_chats:
            stream_name = get_chat_manager().get_stream_name(chat_stream.stream_id) or chat_stream.stream_id
            logger.info(f'Creating new S4UChat for stream: {stream_name}')
            self.s4u_chats[chat_stream.stream_id] = S4UChat(chat_stream)
        return self.s4u_chats[chat_stream.stream_id]