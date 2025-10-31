import os
from typing import Dict, Optional

class LLMConfig:
    """Manages LLM configuration with provider profiles and overrides."""

    def __init__(self):
        self._provider = None
        self._profile = None
        self._custom_models = {}
        self._timeout = None
        self._load_config()

    def _load_config(self):
        """Load configuration from environment variables."""
        self._provider = os.getenv('KATALYST_LLM_PROVIDER', os.getenv('KATALYST_LITELLM_PROVIDER', 'openai')).lower()
        self._profile = os.getenv('KATALYST_LLM_PROFILE', self._provider).lower()
        if self._profile not in PROVIDER_PROFILES:
            logger.warning(f"LLM profile '{self._profile}' not found, using provider '{self._provider}' profile")
            self._profile = self._provider
        if self._profile not in PROVIDER_PROFILES:
            available = ', '.join(PROVIDER_PROFILES.keys())
            raise ValueError(f"Unknown provider profile '{self._profile}'. Available: {available}")
        if os.getenv('KATALYST_REASONING_MODEL'):
            self._custom_models['reasoning'] = os.getenv('KATALYST_REASONING_MODEL')
        if os.getenv('KATALYST_EXECUTION_MODEL'):
            self._custom_models['execution'] = os.getenv('KATALYST_EXECUTION_MODEL')
        if os.getenv('KATALYST_LLM_MODEL_FALLBACK'):
            self._custom_models['fallback'] = os.getenv('KATALYST_LLM_MODEL_FALLBACK')
        try:
            self._timeout = int(os.getenv('KATALYST_LLM_TIMEOUT', os.getenv('KATALYST_LITELLM_TIMEOUT', '0')))
        except ValueError:
            self._timeout = 0
        logger.debug(f'LLM Config loaded - Provider: {self._provider}, Profile: {self._profile}, Custom models: {self._custom_models}')

    def get_model_for_component(self, component: str) -> str:
        """
        Get the appropriate model for a given component.

        Args:
            component: Component name (e.g., 'planner', 'executor')

        Returns:
            Model identifier string
        """
        model_type = COMPONENT_MODEL_MAPPING.get(component.lower(), COMPONENT_MODEL_MAPPING['default'])
        if model_type in self._custom_models:
            return self._custom_models[model_type]
        profile = PROVIDER_PROFILES[self._profile]
        return profile.get(model_type, profile['execution'])

    def get_provider(self) -> str:
        """Get the configured provider."""
        return self._provider

    def get_timeout(self) -> int:
        """Get the configured timeout in seconds."""
        if self._timeout > 0:
            return self._timeout
        profile = PROVIDER_PROFILES[self._profile]
        return profile.get('default_timeout', 45)

    def get_fallback_models(self) -> list[str]:
        """Get list of fallback models."""
        if 'fallback' in self._custom_models:
            return [self._custom_models['fallback']]
        profile = PROVIDER_PROFILES[self._profile]
        return [profile.get('fallback', profile['execution'])]

    def get_api_base(self) -> Optional[str]:
        """Get the API base URL if configured for the provider."""
        api_base = os.getenv('KATALYST_LLM_API_BASE')
        if api_base:
            return api_base
        profile = PROVIDER_PROFILES.get(self._profile, {})
        return profile.get('api_base')

    def get_config_summary(self) -> Dict[str, any]:
        """Get a summary of the current configuration."""
        summary = {'provider': self._provider, 'profile': self._profile, 'timeout': self.get_timeout(), 'models': {'reasoning': self.get_model_for_component('planner'), 'execution': self.get_model_for_component('executor'), 'fallback': self.get_fallback_models()[0]}, 'custom_overrides': self._custom_models}
        api_base = self.get_api_base()
        if api_base:
            summary['api_base'] = api_base
        return summary