
class UnifiedAuthFactory:
    '''Factory for creating model and storage authentication providers.'''
    @staticmethod
    def create_model_auth(provider: str, **kwargs) -> ModelAuthProvider:
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
        provider = provider.lower()
        if provider == 'openai':
            from .openai_auth import OpenAIAuthProvider
            return OpenAIAuthProvider(**kwargs)
        elif provider == 'oci':
            from .oci_auth import OCIModelAuthProvider
            return OCIModelAuthProvider(**kwargs)
        elif provider == 'aws-bedrock':
            from .aws_bedrock_auth import AWSBedrockAuthProvider
            return AWSBedrockAuthProvider(**kwargs)
        elif provider == 'azure-openai':
            from .azure_openai_auth import AzureOpenAIAuthProvider
            return AzureOpenAIAuthProvider(**kwargs)
        elif provider == 'gcp-vertex':
            from .gcp_vertex_auth import GCPVertexAuthProvider
            return GCPVertexAuthProvider(**kwargs)
        else:
            raise ValueError(f'Unsupported model auth provider: {provider}')

    @staticmethod
    def create_storage_auth(provider: str, **kwargs) -> StorageAuthProvider:
        '''Create a storage authentication provider.
        Args:
            provider: Provider type ('oci', 'aws', 'azure', 'gcp', 'github')
            **kwargs: Provider-specific arguments
        Returns:
            StorageAuthProvider instance
        Raises:
            ValueError: If provider is not supported
        '''
        provider = provider.lower()
        if provider == 'oci':
            from .oci_auth import OCIStorageAuthProvider
            return OCIStorageAuthProvider(**kwargs)
        elif provider == 'aws':
            from .aws_auth import AWSStorageAuthProvider
            return AWSStorageAuthProvider(**kwargs)
        elif provider == 'azure':
            from .azure_auth import AzureStorageAuthProvider
            return AzureStorageAuthProvider(**kwargs)
        elif provider == 'gcp':
            from .gcp_auth import GCPStorageAuthProvider
            return GCPStorageAuthProvider(**kwargs)
        elif provider == 'github':
            from .github_auth import GitHubStorageAuthProvider
            return GitHubStorageAuthProvider(**kwargs)
        else:
            raise ValueError(f'Unsupported storage auth provider: {provider}')
