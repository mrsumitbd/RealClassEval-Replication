
class ConversationTurn:

    def __init__(self, user_message, message_index):
        self.user_message = user_message
        self.message_index = message_index

    def _extract_preview(self, message, max_length=50):
        if len(message) <= max_length:
            return message
        else:
            return message[:max_length] + "..."

    def get_preview(self, max_length=50):
        return self._extract_preview(self.user_message, max_length)
