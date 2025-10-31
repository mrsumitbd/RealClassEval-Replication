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
        if not isinstance(provider, str) or not provider.strip():
            raise ValueError('provider must be a non-empty string')
        key = provider.strip().lower().replace('_', '-')

        # Allow some common synonyms
        aliases = {
            'bedrock': 'aws-bedrock',
            'azure': 'azure-openai',
            'vertex': 'gcp-vertex',
            'google-vertex': 'gcp-vertex',
            'google': 'gcp-vertex',
        }
        key = aliases.get(key, key)

        mapping = {
            'openai': OpenAIModelAuthProvider,
            'oci': OCIModelAuthProvider,
            'aws-bedrock': AWSBedrockModelAuthProvider,
            'azure-openai': AzureOpenAIModelAuthProvider,
            'gcp-vertex': GCPVertexModelAuthProvider,
        }

        cls = mapping.get(key)
        if cls is None:
            supported = ', '.join(sorted(mapping.keys()))
            raise ValueError(
                f'Unsupported model auth provider "{provider}". Supported: {supported}')
        return cls(**kwargs)

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
        if not isinstance(provider, str) or not provider.strip():
            raise ValueError('provider must be a non-empty string')
        key = provider.strip().lower()

        # Allow common aliases
        aliases = {
            'gh': 'github',
            'azure-blob': 'azure',
            's3': 'aws',
            'gcs': 'gcp',
        }
        key = aliases.get(key, key)

        mapping = {
            'oci': OCIStorageAuthProvider,
            'aws': AWSStorageAuthProvider,
            'azure': AzureStorageAuthProvider,
            'gcp': GCPStorageAuthProvider,
            'github': GitHubStorageAuthProvider,
        }

        cls = mapping.get(key)
        if cls is None:
            supported = ', '.join(sorted(mapping.keys()))
            raise ValueError(
                f'Unsupported storage auth provider "{provider}". Supported: {supported}')
        return cls(**kwargs)
