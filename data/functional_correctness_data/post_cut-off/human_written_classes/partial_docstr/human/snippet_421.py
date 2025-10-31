from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCompleter

class GuiChatCompleter:
    """Combined GUI completer for chat commands."""

    def __init__(self, message_handler=None):
        self.model_completer = GuiModelCompleter()
        self.agent_completer = GuiAgentCompleter()
        self.jump_completer = GuiJumpCompleter(message_handler)
        self.mcp_completer = GuiMCPCompleter(message_handler)
        self.command_completer = GuiCommandCompleter()

    def get_completions(self, text):
        """Get all completions for the given text."""
        if text.startswith('/model '):
            return self.model_completer.get_completions(text)
        elif text.startswith('/agent '):
            return self.agent_completer.get_completions(text)
        elif text.startswith('/jump '):
            return self.jump_completer.get_completions(text)
        elif text.startswith('/mcp '):
            return self.mcp_completer.get_completions(text)
        elif text.startswith('/'):
            return self.command_completer.get_completions(text)
        else:
            return []

    def create_qt_completer(self, parent=None):
        """Create a QCompleter instance for Qt widgets."""
        completer = QCompleter(parent)
        completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseSensitive)
        return completer