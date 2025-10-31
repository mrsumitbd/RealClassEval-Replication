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
        self.assistant_response = None
        self.message_index = int(
            message_index) if message_index is not None else None
        if self.message_index is not None and self.message_index < 0:
            raise ValueError("message_index must be non-negative")

    def _extract_preview(self, message, max_length=50):
        '''Extract a preview of the message for display in completions.'''
        if max_length is None or max_length < 0:
            max_length = 0

        # Extract textual content from various possible structures
        def to_text(msg):
            if msg is None:
                return ''
            if isinstance(msg, str):
                return msg
            if isinstance(msg, dict):
                for key in ('content', 'text', 'message'):
                    val = msg.get(key)
                    if isinstance(val, str):
                        return val
                return str(msg)
            if isinstance(msg, (list, tuple)):
                parts = []
                for item in msg:
                    if isinstance(item, str):
                        parts.append(item)
                    elif isinstance(item, dict):
                        val = item.get('text') or item.get(
                            'content') or item.get('message')
                        parts.append(val if isinstance(
                            val, str) else str(item))
                    else:
                        parts.append(str(item))
                return ' '.join(parts)
            return str(msg)

        s = to_text(message)
        # Normalize whitespace
        s = ' '.join(s.split())

        if max_length == 0:
            return ''
        if len(s) <= max_length:
            return s
        if max_length == 1:
            return '…'
        return s[: max_length - 1].rstrip() + '…'

    def get_preview(self, max_length=50):
        '''Get a preview of the user message for display in completions.'''
        return self._extract_preview(self.user_message, max_length)
