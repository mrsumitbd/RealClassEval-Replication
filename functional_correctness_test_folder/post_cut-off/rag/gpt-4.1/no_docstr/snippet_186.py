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
        provider = provider.lower()
        if provider == 'openai':
            from model_auth.openai import OpenAIAuthProvider
            return OpenAIAuthProvider(**kwargs)
        elif provider == 'oci':
            from model_auth.oci import OCIModelAuthProvider
            return OCIModelAuthProvider(**kwargs)
        elif provider == 'aws-bedrock':
            from model_auth.aws_bedrock import AWSBedrockAuthProvider
            return AWSBedrockAuthProvider(**kwargs)
        elif provider == 'azure-openai':
            from model_auth.azure_openai import AzureOpenAIAuthProvider
            return AzureOpenAIAuthProvider(**kwargs)
        elif provider == 'gcp-vertex':
            from model_auth.gcp_vertex import GCPVertexAuthProvider
            return GCPVertexAuthProvider(**kwargs)
        else:
            raise ValueError(f"Unsupported model auth provider: {provider}")

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
        provider = provider.lower()
        if provider == 'oci':
            from storage_auth.oci import OCIStorageAuthProvider
            return OCIStorageAuthProvider(**kwargs)
        elif provider == 'aws':
            from storage_auth.aws import AWSStorageAuthProvider
            return AWSStorageAuthProvider(**kwargs)
        elif provider == 'azure':
            from storage_auth.azure import AzureStorageAuthProvider
            return AzureStorageAuthProvider(**kwargs)
        elif provider == 'gcp':
            from storage_auth.gcp import GCPStorageAuthProvider
            return GCPStorageAuthProvider(**kwargs)
        elif provider == 'github':
            from storage_auth.github import GithubStorageAuthProvider
            return GithubStorageAuthProvider(**kwargs)
        else:
            raise ValueError(f"Unsupported storage auth provider: {provider}")
