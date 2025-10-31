from typing import List, Union
import requests


class QwenEmbedding:
    '''千问模型的 Embedding 实现'''

    API_URL = "https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding"

    def __init__(self, config=None):
        '''
        初始化千问 Embedding
        :param config: 配置字典，包含 api_key, model, dimensions 等参数
        '''
        config = config or {}
        self.api_key = config.get("api_key")
        self.model = config.get("model", "text-embedding-v1")
        self.dimensions = config.get("dimensions")
        self._embedding_dim = None

    def embed(self, text: Union[str, List[str]]) -> List[List[float]]:
        '''
        获取文本的向量表示
        :param text: 单个文本字符串或文本列表
        :return: 向量列表
        '''
        if isinstance(text, str):
            input_texts = [text]
        else:
            input_texts = list(text)
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "input": input_texts
        }
        if self.dimensions:
            payload["parameters"] = {"dimensions": self.dimensions}
        resp = requests.post(self.API_URL, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()
        if "output" in data and "embeddings" in data["output"]:
            embeddings = [item["embedding"]
                          for item in data["output"]["embeddings"]]
            if embeddings and self._embedding_dim is None:
                self._embedding_dim = len(embeddings[0])
            return embeddings
        else:
            raise RuntimeError(f"Failed to get embeddings: {data}")

    def encode(self, text: Union[str, List[str]]) -> List[List[float]]:
        '''
        兼容 sentence_transformers 的 encode 方法
        '''
        return self.embed(text)

    def get_embedding_dim(self) -> int:
        '''
        获取向量维度
        '''
        if self._embedding_dim is not None:
            return self._embedding_dim
        # Try to get dimension by embedding a dummy text
        emb = self.embed("test")
        if emb and len(emb) > 0:
            self._embedding_dim = len(emb[0])
            return self._embedding_dim
        raise RuntimeError("Unable to determine embedding dimension.")
