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
        self.user_message = '' if user_message is None else str(user_message)
        self.message_index = message_index

    def _extract_preview(self, message, max_length=50):
        '''Extract a preview of the message for display in completions.'''
        if message is None:
            return ''
        text = str(message).replace('\n', ' ').replace('\r', ' ')
        text = ' '.join(text.split())  # collapse whitespace
        if max_length is None:
            max_length = 50
        try:
            max_length = int(max_length)
        except (TypeError, ValueError):
            max_length = 50
        if max_length <= 0:
            return ''
        if len(text) <= max_length:
            return text
        if max_length <= 3:
            return text[:max_length]
        return text[: max_length - 3].rstrip() + '...'

    def get_preview(self, max_length=50):
        '''Get a preview of the user message for display in completions.'''
        return self._extract_preview(self.user_message, max_length=max_length)
