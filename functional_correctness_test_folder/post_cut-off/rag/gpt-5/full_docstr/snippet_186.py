import importlib
from typing import Any, Dict, Optional, Type


class UnifiedAuthFactory:
    '''Factory for creating model and storage authentication providers.'''

    @staticmethod
    def _import_class(dotted_path: str):
        module_path, _, class_name = dotted_path.rpartition('.')
        if not module_path:
            raise ImportError(f'Invalid import path: {dotted_path}')
        module = importlib.import_module(module_path)
        return getattr(module, class_name)

    @staticmethod
    def _try_import_first(paths: list[str]) -> Optional[type]:
        for path in paths:
            try:
                return UnifiedAuthFactory._import_class(path)
            except Exception:
                continue
        return None

    @staticmethod
    def _instantiate(cls: type, kwargs: Dict[str, Any]) -> Any:
        return cls(**kwargs)

    @staticmethod
    def _normalize_provider(provider: str) -> str:
        return provider.strip().lower().replace('_', '-')

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
        normalized = UnifiedAuthFactory._normalize_provider(provider)
        provider_class = kwargs.pop('provider_class', None)

        if provider_class is not None:
            return UnifiedAuthFactory._instantiate(provider_class, kwargs)

        # Known provider -> expected module/class naming
        module_map = {
            'openai': ('openai', 'OpenAIModelAuthProvider'),
            'oci': ('oci', 'OCIModelAuthProvider'),
            'aws-bedrock': ('aws_bedrock', 'AWSBedrockModelAuthProvider'),
            'azure-openai': ('azure_openai', 'AzureOpenAIModelAuthProvider'),
            'gcp-vertex': ('gcp_vertex', 'GCPVertexModelAuthProvider'),
        }

        if normalized not in module_map:
            supported = ', '.join(sorted(module_map.keys()))
            raise ValueError(
                f'Unsupported model auth provider: {provider}. Supported providers: {supported}')

        module_name, class_name = module_map[normalized]

        # Try multiple plausible import paths to be resilient to package layout
        base_pkg_candidates = [
            # Same package siblings
            '.'.join(__name__.split('.')[:-1]),
            # Common layouts
            'auth',
            'providers',
            'providers.auth',
            'auth.providers',
        ]
        candidate_paths = []
        for base in base_pkg_candidates:
            if base:
                candidate_paths.append(
                    f'{base}.model.{module_name}.{class_name}')
                candidate_paths.append(
                    f'{base}.models.{module_name}.{class_name}')
                candidate_paths.append(
                    f'{base}.model_auth.{module_name}.{class_name}')
        # Also try top-level guesses
        candidate_paths.extend([
            f'model.{module_name}.{class_name}',
            f'models.{module_name}.{class_name}',
            f'model_auth.{module_name}.{class_name}',
            f'{module_name}.{class_name}',
        ])

        cls = UnifiedAuthFactory._try_import_first(candidate_paths)
        if cls is None:
            supported = ', '.join(sorted(module_map.keys()))
            raise ValueError(
                f'Could not locate class for model auth provider "{provider}". Tried: {candidate_paths}')

        return UnifiedAuthFactory._instantiate(cls, kwargs)

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
        normalized = UnifiedAuthFactory._normalize_provider(provider)
        provider_class = kwargs.pop('provider_class', None)

        if provider_class is not None:
            return UnifiedAuthFactory._instantiate(provider_class, kwargs)

        module_map = {
            'oci': ('oci', 'OCIStorageAuthProvider'),
            'aws': ('aws', 'AWSStorageAuthProvider'),
            'azure': ('azure', 'AzureStorageAuthProvider'),
            'gcp': ('gcp', 'GCPStorageAuthProvider'),
            'github': ('github', 'GitHubStorageAuthProvider'),
        }

        if normalized not in module_map:
            supported = ', '.join(sorted(module_map.keys()))
            raise ValueError(
                f'Unsupported storage auth provider: {provider}. Supported providers: {supported}')

        module_name, class_name = module_map[normalized]

        base_pkg_candidates = [
            '.'.join(__name__.split('.')[:-1]),
            'auth',
            'providers',
            'providers.auth',
            'auth.providers',
        ]
        candidate_paths = []
        for base in base_pkg_candidates:
            if base:
                candidate_paths.append(
                    f'{base}.storage.{module_name}.{class_name}')
                candidate_paths.append(
                    f'{base}.storages.{module_name}.{class_name}')
                candidate_paths.append(
                    f'{base}.storage_auth.{module_name}.{class_name}')
        candidate_paths.extend([
            f'storage.{module_name}.{class_name}',
            f'storages.{module_name}.{class_name}',
            f'storage_auth.{module_name}.{class_name}',
            f'{module_name}.{class_name}',
        ])

        cls = UnifiedAuthFactory._try_import_first(candidate_paths)
        if cls is None:
            supported = ', '.join(sorted(module_map.keys()))
            raise ValueError(
                f'Could not locate class for storage auth provider "{provider}". Tried: {candidate_paths}')

        return UnifiedAuthFactory._instantiate(cls, kwargs)
