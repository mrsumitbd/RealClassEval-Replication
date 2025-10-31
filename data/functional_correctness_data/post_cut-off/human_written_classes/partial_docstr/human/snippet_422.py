class GuiCommandCompleter:
    """GUI completer for all commands."""

    def __init__(self):
        self.commands = ['/clear', '/copy', '/debug', '/think', '/consolidate', '/unconsolidate', '/jump', '/agent', '/model', '/mcp', '/file', '/list', '/load', '/help', '/exit', '/quit']

    def get_completions(self, text):
        """Get command completions for GUI."""
        if not text.startswith('/'):
            return []
        completions = []
        for command in self.commands:
            if command.startswith(text):
                completions.append(command)
        return completions