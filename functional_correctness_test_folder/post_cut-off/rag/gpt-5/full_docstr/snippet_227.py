from typing import Any, List, Dict, Optional
import json


class ConversationTurn:
    '''Represents a single turn in the conversation.'''

    def __init__(self, user_message, message_index):
        '''
        Initialize a conversation turn.
        Args:
            user_message: The user's message
            assistant_response: The assistant's response
            message_index: The index of the last message in this turn
        '''
        self.user_message = user_message
        self.message_index = message_index
        self.assistant_response = None

    def _extract_preview(self, message, max_length=50):
        '''Extract a preview of the message for display in completions.'''
        if message is None:
            return ''
        # Try to extract textual content from known structures
        original = message
        if isinstance(message, dict):
            for key in ('content', 'text', 'message', 'body'):
                if key in message:
                    val = message[key]
                    # Flatten nested typical structures
                    if isinstance(val, list):
                        parts = []
                        for item in val:
                            if isinstance(item, str):
                                parts.append(item)
                            elif isinstance(item, dict):
                                for k in ('text', 'content'):
                                    if k in item and isinstance(item[k], str):
                                        parts.append(item[k])
                                        break
                                else:
                                    parts.append(str(item))
                            else:
                                parts.append(str(item))
                        message = ' '.join(parts)
                    else:
                        message = val
                    break
            else:
                try:
                    message = json.dumps(message, ensure_ascii=False)
                except Exception:
                    message = str(message)
        elif isinstance(message, list):
            parts = []
            for item in message:
                if isinstance(item, str):
                    parts.append(item)
                elif isinstance(item, dict):
                    for k in ('text', 'content', 'message'):
                        if k in item and isinstance(item[k], str):
                            parts.append(item[k])
                            break
                    else:
                        parts.append(str(item))
                else:
                    parts.append(str(item))
            message = ' '.join(parts)

        if not isinstance(message, str):
            try:
                message = str(message)
            except Exception:
                message = str(type(original))

        # Normalize whitespace
        preview = ' '.join(message.split())

        if max_length is None:
            return preview
        if not isinstance(max_length, int) or max_length <= 0:
            return ''
        if len(preview) <= max_length:
            return preview

        suffix = '...'
        if max_length <= len(suffix):
            return preview[:max_length]
        return preview[:max_length - len(suffix)] + suffix

    def get_preview(self, max_length=50):
        '''Get a preview of the user message for display in completions.'''
        return self._extract_preview(self.user_message, max_length=max_length)
