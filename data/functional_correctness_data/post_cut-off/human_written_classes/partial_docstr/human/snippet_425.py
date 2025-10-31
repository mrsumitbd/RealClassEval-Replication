from AgentCrew.modules.llm.model_registry import ModelRegistry

class GuiModelCompleter:
    """GUI completer for model commands."""

    def __init__(self):
        self.registry = ModelRegistry.get_instance()

    def get_completions(self, text):
        """Get model completions for GUI."""
        if not text.startswith('/model '):
            return []
        word_after_command = text[7:]
        all_models = []
        for provider in self.registry.get_providers():
            for model in self.registry.get_models_by_provider(provider):
                all_models.append((model.id, model.name, provider))
        completions = []
        for model_id, model_name, provider in all_models:
            if model_id.startswith(word_after_command):
                completions.append(f'{provider}/{model_id}')
        return completions