
from typing import Any


class UnifiedAuthFactory:
    """Factory for creating model and storage authentication providers."""

    @staticmethod
    def create_model_auth(provider: str, **kwargs) -> 'ModelAuthProvider':
        """Create a model endpoint authentication provider.

        Args:
            provider: Provider type ('openai', 'oci', 'aws-bedrock',
                'azure-openai', 'gcp-vertex')
            **kwargs: Provider-specific arguments

        Returns:
            ModelAuthProvider instance

        Raises:
            ValueError: If provider is not supported
        """
        model_auth_providers = {
            'openai': OpenAIModelAuthProvider,
            'oci': OCIModelAuthProvider,
            'aws-bedrock': AWSBedrockModelAuthProvider,
            'azure-openai': AzureOpenAIModelAuthProvider,
            'gcp-vertex': GCPVertexModelAuthProvider
        }
        model_auth_provider_class = model_auth_providers.get(provider.lower())
        if not model_auth_provider_class:
            raise ValueError(f'Unsupported model auth provider: {provider}')
        return model_auth_provider_class(**kwargs)

    @staticmethod
    def create_storage_auth(provider: str, **kwargs) -> 'StorageAuthProvider':
        """Create a storage authentication provider.

        Args:
            provider: Provider type ('oci', 'aws', 'azure', 'gcp', 'github')
            **kwargs: Provider-specific arguments

        Returns:
            StorageAuthProvider instance

        Raises:
            ValueError: If provider is not supported
        """
        storage_auth_providers = {
            'oci': OCIStorageAuthProvider,
            'aws': AWSStorageAuthProvider,
            'azure': AzureStorageAuthProvider,
            'gcp': GCPStorageAuthProvider,
            'github': GitHubStorageAuthProvider
        }
        storage_auth_provider_class = storage_auth_providers.get(
            provider.lower())
        if not storage_auth_provider_class:
            raise ValueError(f'Unsupported storage auth provider: {provider}')
        return storage_auth_provider_class(**kwargs)
