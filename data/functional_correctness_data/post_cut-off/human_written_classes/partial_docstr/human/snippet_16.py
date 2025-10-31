from lpm_kernel.api.repositories.user_llm_config_repository import UserLLMConfigRepository
from typing import Optional
from lpm_kernel.api.dto.user_llm_config_dto import UserLLMConfigDTO, UpdateUserLLMConfigDTO

class UserLLMConfigService:
    """User LLM Configuration Service"""

    def __init__(self):
        self.repository = UserLLMConfigRepository()

    def get_available_llm(self) -> Optional[UserLLMConfigDTO]:
        """Get available LLM configuration
        Since we only have one default configuration now (ID=1), just return it
        """
        return self.repository.get_default_config()

    def update_config(self, config_id: int, dto: UpdateUserLLMConfigDTO) -> UserLLMConfigDTO:
        """Update configuration or create if not exists

        This method ensures that only one configuration record exists in the database.
        If the configuration with the given ID doesn't exist, it will be created.

        Args:
            config_id: Configuration ID (should be 1)
            dto: UpdateUserLLMConfigDTO object

        Returns:
            Updated or created configuration
        """
        self._ensure_single_record()
        return self.repository.update(config_id, dto)

    def delete_key(self, config_id: int=1) -> Optional[UserLLMConfigDTO]:
        """Delete API key from the configuration

        This method removes the API key and related fields from the configuration.

        Args:
            config_id: Configuration ID (default is 1)

        Returns:
            Updated configuration with key removed
        """
        self._ensure_single_record()
        config = self.repository.get_default_config()
        if not config:
            return None
        return self.repository.delete(config_id)

    def _ensure_single_record(self):
        """Ensure that only one configuration record exists in the database"""
        count = self.repository.count()
        if count != 1:
            from lpm_kernel.common.logging import logger
            logger.warning(f'Found {count} LLM configurations in the database. Only one should exist.')