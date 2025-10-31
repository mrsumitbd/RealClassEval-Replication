
import json
from typing import List, Union, Dict, Any, Optional
import requests


class QwenEmbedding:
    '''千问模型的 Embedding 实现'''

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化千问 Embedding
        :param config: 配置字典，包含 api_key, model, dimensions 等参数
        """
        config = config or {}
        self.api_key: str = config.get("api_key", "")
        self.model: str = config.get("model", "qwen-1.5-7b-chat")
        self.dimensions: Optional[int] = config.get("dimensions")
        self.endpoint: str = config.get(
            "endpoint", "https://qwenapi.qwen.com/api/v1/embeddings"
        )
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            }
        )

    def _embed_single(self, text: str) -> List[float]:
        payload = {"model": self.model, "input": text}
        resp = self._session.post(self.endpoint, data=json.dumps(payload))
        resp.raise_for_status()
        data = resp.json()
        # Expected format: {"data":[{"embedding":[...]}]}
        if "data" not in data or not data["data"]:
            raise ValueError(f"Unexpected response format: {data}")
        embedding = data["data"][0].get("embedding")
        if embedding is None:
            raise ValueError(f"No embedding found in response: {data}")
        return embedding

    def embed(self, text: Union[str, List[str]]) -> List[List[float]]:
        """
        获取文本的向量表示
        :param text: 单个文本字符串或文本列表
        :return: 向量列表
        """
        if isinstance(text, str):
            texts = [text]
        else:
            texts = text

        embeddings = []
        for t in texts:
            embeddings.append(self._embed_single(t))

        # Update dimensions if not set
        if self.dimensions is None and embeddings:
            self.dimensions = len(embeddings[0])

        return embeddings

    def encode(self, text: Union[str, List[str]]) -> List[List[float]]:
        """
        兼容 sentence_transformers 的 encode 方法
        """
        return self.embed(text)

    def get_embedding_dim(self) -> int:
        """
        返回嵌入向量的维度
        """
        if self.dimensions is not None:
            return self.dimensions
        raise ValueError("Embedding dimension is not set. Run embed() first.")
