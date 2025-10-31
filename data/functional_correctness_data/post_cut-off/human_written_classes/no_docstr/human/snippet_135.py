class VectorStoreFactory:
    provider_to_class = {'chroma': 'core.memory_rag.config.vector_config.ChromaDB'}

    @classmethod
    def create(cls, provider_name, config):
        class_type = cls.provider_to_class.get(provider_name)
        if class_type:
            if not isinstance(config, dict):
                if hasattr(config, 'model_dump'):
                    config = config.model_dump()
                else:
                    return config
            vector_store_instance = load_class(class_type)
            return vector_store_instance(**config)
        else:
            raise ValueError(f'Unsupported VectorStore provider: {provider_name}')

    @classmethod
    def reset(cls, instance):
        instance.reset()
        return instance