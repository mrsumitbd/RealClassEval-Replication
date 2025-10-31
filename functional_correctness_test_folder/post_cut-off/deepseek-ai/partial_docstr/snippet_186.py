
class UnifiedAuthFactory:

    @staticmethod
    def create_model_auth(provider: str, **kwargs) -> ModelAuthProvider:
        if provider == 'openai':
            return OpenAIAuth(**kwargs)
        elif provider == 'huggingface':
            return HuggingFaceAuth(**kwargs)
        elif provider == 'anthropic':
            return AnthropicAuth(**kwargs)
        else:
            raise ValueError(f"Unsupported model provider: {provider}")

    @staticmethod
    def create_storage_auth(provider: str, **kwargs) -> StorageAuthProvider:
        if provider == 'oci':
            return OCIAuth(**kwargs)
        elif provider == 'aws':
            return AWSAuth(**kwargs)
        elif provider == 'azure':
            return AzureAuth(**kwargs)
        elif provider == 'gcp':
            return GCPAuth(**kwargs)
        elif provider == 'github':
            return GitHubAuth(**kwargs)
        else:
            raise ValueError(f"Unsupported storage provider: {provider}")
