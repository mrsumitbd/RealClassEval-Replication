class GuiAgentCompleter:
    """GUI completer for agent commands."""

    def __init__(self):
        from AgentCrew.modules.agents.manager import AgentManager
        self.agent_manager = AgentManager.get_instance()

    def get_completions(self, text):
        """Get agent completions for GUI."""
        if not text.startswith('/agent '):
            return []
        word_after_command = text[7:]
        completions = []
        for agent_name, agent in self.agent_manager.agents.items():
            if agent_name.startswith(word_after_command):
                completions.append(agent_name)
        return completions