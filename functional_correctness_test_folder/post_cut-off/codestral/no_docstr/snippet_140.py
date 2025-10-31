
from typing import Union, List
import torch
from transformers import AutoModel, AutoTokenizer


class QwenEmbedding:

    def __init__(self, config=None):
        self.config = config or {}
        self.model_name = self.config.get('model_name', 'Qwen/Qwen-7B')
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)
        self.model.eval()

    def embed(self, text: Union[str, List[str]]) -> List[List[float]]:
        if isinstance(text, str):
            text = [text]
        inputs = self.tokenizer(text, return_tensors="pt",
                                padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1).tolist()
        return embeddings

    def encode(self, text: Union[str, List[str]]) -> List[List[float]]:
        return self.embed(text)

    def get_embedding_dim(self) -> int:
        return self.model.config.hidden_size
