from __future__ import annotations
from types import SimpleNamespace


class UnifiedAuthFactory:
    '''Factory for creating model and storage authentication providers.'''
    @staticmethod
    def create_model_auth(provider: str, **kwargs) -> 'ModelAuthProvider':
        '''Create a model endpoint authentication provider.
        Args:
            provider: Provider type ('openai', 'oci', 'aws-bedrock',
                'azure-openai', 'gcp-vertex')
            **kwargs: Provider-specific arguments
        Returns:
            ModelAuthProvider instance
        Raises:
            ValueError: If provider is not supported
        '''
        supported = {
            'openai',
            'oci',
            'aws-bedrock',
            'azure-openai',
            'gcp-vertex',
        }
        if provider not in supported:
            raise ValueError(f"Unsupported model auth provider: {provider}")

        try:
            if provider == 'openai':
                # Try common class names and paths
                for mod, cls in (
                    ('openai_auth', 'OpenAIModelAuth'),
                    ('providers.model.openai', 'OpenAIModelAuth'),
                    ('auth.model.openai', 'OpenAIModelAuth'),
                ):
                    try:
                        module = __import__(mod, fromlist=[cls])
                        return getattr(module, cls)(**kwargs)
                    except Exception:
                        continue

            elif provider == 'oci':
                for mod, cls in (
                    ('oci_auth', 'OCIModelAuth'),
                    ('providers.model.oci', 'OCIModelAuth'),
                    ('auth.model.oci', 'OCIModelAuth'),
                ):
                    try:
                        module = __import__(mod, fromlist=[cls])
                        return getattr(module, cls)(**kwargs)
                    except Exception:
                        continue

            elif provider == 'aws-bedrock':
                for mod, cls in (
                    ('bedrock_auth', 'BedrockModelAuth'),
                    ('providers.model.aws', 'BedrockModelAuth'),
                    ('auth.model.aws_bedrock', 'BedrockModelAuth'),
                ):
                    try:
                        module = __import__(mod, fromlist=[cls])
                        return getattr(module, cls)(**kwargs)
                    except Exception:
                        continue

            elif provider == 'azure-openai':
                for mod, cls in (
                    ('azure_openai_auth', 'AzureOpenAIModelAuth'),
                    ('providers.model.azure', 'AzureOpenAIModelAuth'),
                    ('auth.model.azure_openai', 'AzureOpenAIModelAuth'),
                ):
                    try:
                        module = __import__(mod, fromlist=[cls])
                        return getattr(module, cls)(**kwargs)
                    except Exception:
                        continue

            elif provider == 'gcp-vertex':
                for mod, cls in (
                    ('vertex_auth', 'VertexAIModelAuth'),
                    ('providers.model.gcp', 'VertexAIModelAuth'),
                    ('auth.model.gcp_vertex', 'VertexAIModelAuth'),
                ):
                    try:
                        module = __import__(mod, fromlist=[cls])
                        return getattr(module, cls)(**kwargs)
                    except Exception:
                        continue
        except Exception as e:
            raise

        # Fallback generic provider if specific implementation is unavailable
        class _GenericModelAuth(SimpleNamespace):
            def __init__(self, provider: str, **params):
                super().__init__(provider=provider, params=params)

        return _GenericModelAuth(provider=provider, **kwargs)

    @staticmethod
    def create_storage_auth(provider: str, **kwargs) -> 'StorageAuthProvider':
        '''Create a storage authentication provider.
        Args:
            provider: Provider type ('oci', 'aws', 'azure', 'gcp', 'github')
            **kwargs: Provider-specific arguments
        Returns:
            StorageAuthProvider instance
        Raises:
            ValueError: If provider is not supported
        '''
        supported = {
            'oci',
            'aws',
            'azure',
            'gcp',
            'github',
        }
        if provider not in supported:
            raise ValueError(f"Unsupported storage auth provider: {provider}")

        try:
            if provider == 'oci':
                for mod, cls in (
                    ('oci_storage_auth', 'OCIStorageAuth'),
                    ('providers.storage.oci', 'OCIStorageAuth'),
                    ('auth.storage.oci', 'OCIStorageAuth'),
                ):
                    try:
                        module = __import__(mod, fromlist=[cls])
                        return getattr(module, cls)(**kwargs)
                    except Exception:
                        continue

            elif provider == 'aws':
                for mod, cls in (
                    ('aws_storage_auth', 'AWSStorageAuth'),
                    ('providers.storage.aws', 'AWSStorageAuth'),
                    ('auth.storage.aws', 'AWSStorageAuth'),
                ):
                    try:
                        module = __import__(mod, fromlist=[cls])
                        return getattr(module, cls)(**kwargs)
                    except Exception:
                        continue

            elif provider == 'azure':
                for mod, cls in (
                    ('azure_storage_auth', 'AzureStorageAuth'),
                    ('providers.storage.azure', 'AzureStorageAuth'),
                    ('auth.storage.azure', 'AzureStorageAuth'),
                ):
                    try:
                        module = __import__(mod, fromlist=[cls])
                        return getattr(module, cls)(**kwargs)
                    except Exception:
                        continue

            elif provider == 'gcp':
                for mod, cls in (
                    ('gcp_storage_auth', 'GCPStorageAuth'),
                    ('providers.storage.gcp', 'GCPStorageAuth'),
                    ('auth.storage.gcp', 'GCPStorageAuth'),
                ):
                    try:
                        module = __import__(mod, fromlist=[cls])
                        return getattr(module, cls)(**kwargs)
                    except Exception:
                        continue

            elif provider == 'github':
                for mod, cls in (
                    ('github_storage_auth', 'GitHubStorageAuth'),
                    ('providers.storage.github', 'GitHubStorageAuth'),
                    ('auth.storage.github', 'GitHubStorageAuth'),
                ):
                    try:
                        module = __import__(mod, fromlist=[cls])
                        return getattr(module, cls)(**kwargs)
                    except Exception:
                        continue
        except Exception as e:
            raise

        # Fallback generic provider if specific implementation is unavailable
        class _GenericStorageAuth(SimpleNamespace):
            def __init__(self, provider: str, **params):
                super().__init__(provider=provider, params=params)

        return _GenericStorageAuth(provider=provider, **kwargs)
