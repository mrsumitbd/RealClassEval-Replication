from uuid import uuid4
from typing import List, Dict, Any, Optional, Tuple, Union

class MemorySystem:

    def __init__(self):
        self.conversations: Dict[str, List[Dict[str, str]]] = {}

    def add_message(self, conversation_id: str, message: Dict[str, str]):
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        self.conversations[conversation_id].append(message)

    def get_conversation(self, conversation_id: str) -> List[Dict[str, str]]:
        return self.conversations.get(conversation_id, [])

    def duplicate_conversation_excluding_last_turn(self, conversation_id: str) -> str:
        original_conversation = self.get_conversation(conversation_id)
        new_conversation_id = str(uuid4())
        new_conversation = original_conversation[:-2]
        self.conversations[new_conversation_id] = new_conversation
        return new_conversation_id