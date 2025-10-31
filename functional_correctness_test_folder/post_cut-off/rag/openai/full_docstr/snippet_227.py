
class ConversationTurn:
    '''Represents a single turn in the conversation.'''

    def __init__(self, user_message, message_index):
        '''
        Initialize a conversation turn.
        Args:
            user_message: The user's message
            message_index: The index of the last message in this turn
        '''
        self.user_message = user_message
        self.message_index = message_index

    def _extract_preview(self, message, max_length=50):
        '''Extract a preview of the message for display in completions.'''
        if message is None:
            return ''
        # Ensure we are working with a string
        text = str(message).strip()
        if len(text) <= max_length:
            return text
        # Truncate and add ellipsis
        return text[:max_length] + '...'

    def get_preview(self, max_length=50):
        '''Get a preview of the user message for display in completions.'''
        return self._extract_preview(self.user_message, max_length)
