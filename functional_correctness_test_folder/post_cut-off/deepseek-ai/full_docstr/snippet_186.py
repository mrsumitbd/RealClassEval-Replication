
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
        if provider == 'openai':
            return OpenAIAuthProvider(**kwargs)
        elif provider == 'oci':
            return OCIModelAuthProvider(**kwargs)
        elif provider == 'aws-bedrock':
            return AWSBedrockAuthProvider(**kwargs)
        elif provider == 'azure-openai':
            return AzureOpenAIAuthProvider(**kwargs)
        elif provider == 'gcp-vertex':
            return GCPVertexAuthProvider(**kwargs)
        else:
            raise ValueError(f"Unsupported model auth provider: {provider}")

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
        if provider == 'oci':
            return OCIStorageAuthProvider(**kwargs)
        elif provider == 'aws':
            return AWSStorageAuthProvider(**kwargs)
        elif provider == 'azure':
            return AzureStorageAuthProvider(**kwargs)
        elif provider == 'gcp':
            return GCPStorageAuthProvider(**kwargs)
        elif provider == 'github':
            return GitHubStorageAuthProvider(**kwargs)
        else:
            raise ValueError(f"Unsupported storage auth provider: {provider}")
