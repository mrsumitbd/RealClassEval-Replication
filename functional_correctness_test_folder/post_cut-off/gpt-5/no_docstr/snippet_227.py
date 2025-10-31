class ConversationTurn:

    def __init__(self, user_message, message_index):
        self.user_message = '' if user_message is None else str(user_message)
        if not isinstance(message_index, int):
            try:
                message_index = int(message_index)
            except Exception:
                raise TypeError("message_index must be an int")
        self.message_index = message_index

    def _extract_preview(self, message, max_length=50):
        if max_length is None:
            max_length = 50
        try:
            max_length = int(max_length)
        except Exception:
            raise TypeError("max_length must be an int")
        if max_length < 0:
            raise ValueError("max_length must be non-negative")

        text = '' if message is None else str(message)

        import re
        text = re.sub(r'\s+', ' ', text).strip()

        if len(text) <= max_length:
            return text
        if max_length == 0:
            return ''
        if max_length <= 3:
            return '.' * max_length
        return text[: max_length - 3] + '...'

    def get_preview(self, max_length=50):
        return self._extract_preview(self.user_message, max_length)
