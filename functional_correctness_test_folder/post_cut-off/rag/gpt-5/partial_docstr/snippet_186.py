class UnifiedAuthFactory:
    '''Factory for creating model and storage authentication providers.'''

    @staticmethod
    def _normalize_model_provider(provider: str) -> str:
        p = (provider or '').strip().lower()
        synonyms = {
            'aws': 'aws-bedrock',
            'bedrock': 'aws-bedrock',
            'azure': 'azure-openai',
            'azure_openai': 'azure-openai',
            'azureopenai': 'azure-openai',
            'gcp': 'gcp-vertex',
            'vertex': 'gcp-vertex',
            'vertexai': 'gcp-vertex',
            'google': 'gcp-vertex',
            'oracle': 'oci',
        }
        return synonyms.get(p, p)

    @staticmethod
    def _normalize_storage_provider(provider: str) -> str:
        p = (provider or '').strip().lower()
        synonyms = {
            'amazon': 'aws',
            'aws-s3': 'aws',
            's3': 'aws',
            'google': 'gcp',
            'gcs': 'gcp',
            'github': 'github',
            'gh': 'github',
        }
        return synonyms.get(p, p)

    @staticmethod
    def _load_provider_class(kind: str, provider_key: str, class_name_candidates: list):
        import importlib

        # Try to locate class in current module globals first (in case classes are re-exported)
        for cls_name in class_name_candidates:
            if cls_name in globals():
                return globals()[cls_name]

        # Build module candidate paths
        seg = provider_key.replace('-', '_')
        module_segments = [
            seg,
            f'{kind}',
            f'{kind}_{seg}',
            f'{kind}.{seg}',
            f'{kind}s',
            f'{kind}s.{seg}',
            f'auth.{kind}',
            f'auth.{kind}.{seg}',
            f'providers.{kind}',
            f'providers.{kind}.{seg}',
            f'{kind}_auth',
            f'{kind}_auth.{seg}',
            f'{kind}_providers',
            f'{kind}_providers.{seg}',
        ]

        # If this module is part of a package, try relative base package variants
        base_pkg = None
        if '.' in __name__:
            base_pkg = __name__.rsplit('.', 1)[0]

        module_candidates = []
        for segm in module_segments:
            module_candidates.append(segm)
            if base_pkg:
                module_candidates.append(f'{base_pkg}.{segm}')

        seen = set()
        module_candidates = [
            m for m in module_candidates if not (m in seen or seen.add(m))]

        for module_path in module_candidates:
            try:
                mod = importlib.import_module(module_path)
            except Exception:
                continue
            for cls_name in class_name_candidates:
                cls = getattr(mod, cls_name, None)
                if cls is not None:
                    return cls

        return None

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
        provider_key = UnifiedAuthFactory._normalize_model_provider(provider)
        class_candidates_map = {
            'openai': ['OpenAIModelAuthProvider', 'OpenAIAuthProvider', 'OpenAIAuth'],
            'oci': ['OCIModelAuthProvider', 'OCIAuthProvider', 'OCIAuth'],
            'aws-bedrock': ['AWSBedrockModelAuthProvider', 'BedrockModelAuthProvider', 'AWSBedrockAuthProvider', 'BedrockAuthProvider'],
            'azure-openai': ['AzureOpenAIModelAuthProvider', 'AzureOpenAIAuthProvider', 'AzureOpenAIAuth'],
            'gcp-vertex': ['GCPVertexModelAuthProvider', 'VertexAIModelAuthProvider', 'GCPVertexAuthProvider', 'VertexAIAuthProvider'],
        }

        # Allow explicit class override via kwargs
        override_cls = kwargs.pop('provider_class', None) or kwargs.pop(
            'class_', None) or kwargs.pop('cls', None)
        if override_cls is not None:
            return override_cls(**kwargs)

        candidates = class_candidates_map.get(provider_key)
        if not candidates:
            raise ValueError(f'Unsupported model provider: {provider}')

        cls = UnifiedAuthFactory._load_provider_class(
            'model', provider_key, candidates)
        if cls is None:
            raise ValueError(f'Unsupported model provider: {provider}')
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
        provider_key = UnifiedAuthFactory._normalize_storage_provider(provider)
        class_candidates_map = {
            'oci': ['OCIStorageAuthProvider', 'OCIAuthProvider', 'OCIStorageAuth'],
            'aws': ['AWSStorageAuthProvider', 'S3StorageAuthProvider', 'AWSAuthProvider'],
            'azure': ['AzureStorageAuthProvider', 'AzureAuthProvider'],
            'gcp': ['GCPStorageAuthProvider', 'GCSStorageAuthProvider', 'GCPAuthProvider'],
            'github': ['GitHubStorageAuthProvider', 'GithubStorageAuthProvider', 'GitHubAuthProvider', 'GithubAuthProvider'],
        }

        # Allow explicit class override via kwargs
        override_cls = kwargs.pop('provider_class', None) or kwargs.pop(
            'class_', None) or kwargs.pop('cls', None)
        if override_cls is not None:
            return override_cls(**kwargs)

        candidates = class_candidates_map.get(provider_key)
        if not candidates:
            raise ValueError(f'Unsupported storage provider: {provider}')

        cls = UnifiedAuthFactory._load_provider_class(
            'storage', provider_key, candidates)
        if cls is None:
            raise ValueError(f'Unsupported storage provider: {provider}')
        return cls(**kwargs)
