from typing import Dict, List


class ModelConfig:
    _CATALOG: Dict[str, Dict[str, str]] = {
        # OpenAI
        "gpt-4o": {"provider": "openai", "family": "gpt-4o", "tier": "standard"},
        "gpt-4o-mini": {"provider": "openai", "family": "gpt-4o", "tier": "mini"},
        "gpt-4.1": {"provider": "openai", "family": "gpt-4.1", "tier": "standard"},
        "gpt-4.1-mini": {"provider": "openai", "family": "gpt-4.1", "tier": "mini"},
        "gpt-3.5-turbo": {"provider": "openai", "family": "gpt-3.5", "tier": "standard"},
        # Anthropic
        "claude-3-opus-20240229": {"provider": "anthropic", "family": "claude-3", "tier": "opus"},
        "claude-3-sonnet-20240229": {"provider": "anthropic", "family": "claude-3", "tier": "sonnet"},
        "claude-3-haiku-20240307": {"provider": "anthropic", "family": "claude-3", "tier": "haiku"},
        "claude-3-5-sonnet-20240620": {"provider": "anthropic", "family": "claude-3.5", "tier": "sonnet"},
        # Google
        "gemini-1.5-pro": {"provider": "google", "family": "gemini-1.5", "tier": "pro"},
        "gemini-1.5-flash": {"provider": "google", "family": "gemini-1.5", "tier": "flash"},
        # Meta
        "llama-3-70b-instruct": {"provider": "meta", "family": "llama-3", "tier": "70b-instruct"},
        "llama-3-8b-instruct": {"provider": "meta", "family": "llama-3", "tier": "8b-instruct"},
        # Mistral
        "mistral-large": {"provider": "mistral", "family": "mistral", "tier": "large"},
        "mistral-small": {"provider": "mistral", "family": "mistral", "tier": "small"},
    }

    def __init__(self, model_name: str):
        if not isinstance(model_name, str) or not model_name.strip():
            raise ValueError("model_name must be a non-empty string")
        self.model_name = model_name.strip()
        self.info = self._get_model_info(self.model_name)

    def _get_model_info(self, model_name: str) -> Dict[str, str]:
        name = model_name.strip()
        if name in self._CATALOG:
            return {"name": name, **self._CATALOG[name]}
        # fallback: case-insensitive match
        lowered = {k.lower(): k for k in self._CATALOG.keys()}
        key = lowered.get(name.lower())
        if key:
            return {"name": key, **self._CATALOG[key]}
        raise KeyError(f"Unsupported model: {model_name}")

    @classmethod
    def get_supported_models(cls) -> List[str]:
        return sorted(cls._CATALOG.keys())
