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
        self.message_index = int(message_index) if isinstance(
            message_index, (int, float, str)) and str(message_index).isdigit() else message_index

    def _extract_preview(self, message, max_length=50):
        '''Extract a preview of the message for display in completions.'''
        def to_text(msg):
            if msg is None:
                return ''
            if isinstance(msg, str):
                return msg
            if isinstance(msg, (list, tuple)):
                parts = []
                for item in msg:
                    t = to_text(item)
                    if t:
                        parts.append(t)
                return ' '.join(parts)
            if isinstance(msg, dict):
                # Prefer common text-bearing keys
                for key in ('text', 'content', 'message', 'value', 'input'):
                    if key in msg:
                        v = msg.get(key)
                        t = to_text(v)
                        if t:
                            return t
                # Fallback: concatenate any textual values
                parts = []
                for v in msg.values():
                    t = to_text(v)
                    if t:
                        parts.append(t)
                return ' '.join(parts)
            return str(msg)

        try:
            ml = int(max_length)
        except Exception:
            ml = 50
        if ml <= 0:
            return ''

        s = to_text(message)
        s = ' '.join(s.split())  # collapse whitespace

        if len(s) <= ml:
            return s
        if ml == 1:
            return '…'
        return s[:ml - 1] + '…'

    def get_preview(self, max_length=50):
        '''Get a preview of the user message for display in completions.'''
        return self._extract_preview(self.user_message, max_length=max_length)
