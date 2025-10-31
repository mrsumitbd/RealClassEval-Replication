class ConversationTurn:

    def __init__(self, user_message, message_index):
        self.user_message = user_message
        self.message_index = message_index

    def _extract_preview(self, message, max_length=50):
        '''Extract a preview of the message for display in completions.'''
        if message is None:
            return ""
        text = str(message)
        # Normalize whitespace for a clean preview
        text = " ".join(text.split())

        if not isinstance(max_length, int) or max_length < 0:
            max_length = 50

        if len(text) <= max_length:
            return text

        if max_length == 0:
            return ""
        if max_length == 1:
            return text[:1]

        return text[: max_length - 1].rstrip() + "…"

    def get_preview(self, max_length=50):
        return self._extract_preview(self.user_message, max_length)
