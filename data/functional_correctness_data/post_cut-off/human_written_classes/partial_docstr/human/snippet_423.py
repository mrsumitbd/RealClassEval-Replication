class GuiJumpCompleter:
    """GUI completer for jump commands."""

    def __init__(self, message_handler=None):
        self.message_handler = message_handler

    def get_completions(self, text):
        """Get jump completions for GUI."""
        if not text.startswith('/jump '):
            return []
        word_after_command = text[6:]
        conversation_turns = self.message_handler.conversation_turns if self.message_handler else []
        completions = []
        for i, turn in enumerate(conversation_turns, 1):
            turn_str = str(i)
            if turn_str.startswith(word_after_command):
                completions.append(turn_str)
        return completions