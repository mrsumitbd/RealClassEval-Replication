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

    def _extract_preview(self, message, max_length=50):
        '''Extract a preview of the message for display in completions.'''
        if message is None:
            return ""
        msg_str = str(message)
        if len(msg_str) <= max_length:
            return msg_str
        return msg_str[:max_length - 3] + "..."

    def get_preview(self, max_length=50):
        '''Get a preview of the user message for display in completions.'''
        return self._extract_preview(self.user_message, max_length=max_length)
