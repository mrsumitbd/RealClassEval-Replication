
from typing import Union, List


class QwenEmbedding:

    def __init__(self, config=None):
        # For demonstration purposes, assume a default embedding dimension and model
        self.embedding_dim = 128  # Default embedding dimension
        self.model = None  # Initialize model as None

        # If a configuration is provided, update the embedding dimension and model accordingly
        if config is not None:
            self.embedding_dim = config.get(
                'embedding_dim', self.embedding_dim)
            # Here you would typically load a model based on the config
            # For example: self.model = load_model(config['model_name'])

    def embed(self, text: Union[str, List[str]]) -> List[List[float]]:
        # For demonstration, a simple embedding function is used
        # In a real scenario, this would involve calling a model's embedding function
        if isinstance(text, str):
            # Simulate embedding a single string
            return [[0.1 * i for i in range(self.embedding_dim)]]
        else:
            # Simulate embedding a list of strings
            return [[0.1 * i + j / 100 for i in range(self.embedding_dim)] for j in range(len(text))]

    def encode(self, text: Union[str, List[str]]) -> List[List[float]]:
        # For this example, encode is an alias for embed
        return self.embed(text)

    def get_embedding_dim(self) -> int:
        return self.embedding_dim


# Example usage
if __name__ == "__main__":
    qwen = QwenEmbedding({'embedding_dim': 10})
    print(qwen.embed("Hello, world!"))
    print(qwen.encode(["Hello", "world!"]))
    print(qwen.get_embedding_dim())
