class ConversationTurn:
    """Represents a single turn in the conversation."""

    def __init__(self, user_message, message_index):
        """
        Initialize a conversation turn.

        Args:
            user_message: The user's message
            assistant_response: The assistant's response
            message_index: The index of the last message in this turn
        """
        self.user_message_preview = self._extract_preview(user_message)
        self.message_index = message_index

    def _extract_preview(self, message, max_length=50):
        """Extract a preview of the message for display in completions."""
        if isinstance(message, dict) and 'content' in message:
            content = message['content']
            if isinstance(content, list):
                for item in content:
                    if item.get('type') == 'text':
                        text = item.get('text', '')
                        break
                else:
                    text = str(content)
            else:
                text = str(content)
        else:
            text = str(message)
        if len(text) > max_length:
            return text[:max_length] + '...'
        return text

    def get_preview(self, max_length=50):
        """Get a preview of the user message for display in completions."""
        return self.user_message_preview