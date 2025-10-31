class GuiMCPCompleter:
    """GUI completer for MCP commands."""

    def __init__(self, message_handler=None):
        if message_handler:
            self.mcp_service = message_handler.mcp_manager.mcp_service
        else:
            self.mcp_service = None

    def get_completions(self, text):
        """Get MCP completions for GUI."""
        if not text.startswith('/mcp '):
            return []
        word_after_command = text[5:]
        completions = []
        if self.mcp_service and hasattr(self.mcp_service, 'server_prompts'):
            for server_id, prompts in self.mcp_service.server_prompts.items():
                for prompt in prompts:
                    prompt_name = getattr(prompt, 'name', None) or prompt.get('name')
                    if prompt_name:
                        full_name = f'{server_id}/{prompt_name}'
                        if full_name.startswith(word_after_command):
                            completions.append(full_name)
        return completions