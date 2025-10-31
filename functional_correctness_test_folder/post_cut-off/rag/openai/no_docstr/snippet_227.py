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
        if not message:
            return ''
        preview = message.strip()
        if len(preview) > max_length:
            return preview[:max_length] + '…'
        return preview

    def get_preview(self, max_length=50):
        '''Get a preview of the user message for display in completions.'''
        return self._extract_preview(self.user_message, max_length)
