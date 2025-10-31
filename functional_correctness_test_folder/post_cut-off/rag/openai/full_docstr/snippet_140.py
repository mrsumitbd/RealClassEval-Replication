
import json
from typing import List, Union, Dict, Any

import requests


class QwenEmbedding:
    """千问模型的 Embedding 实现"""

    def __init__(self, config: Dict[str, Any] | None = None):
        """
        初始化千问 Embedding

        :param config: 配置字典，包含 api_key, model, dimensions 等参数
        """
        config = config or {}
        self.api_key: str = config.get("api_key", "")
        self.model: str = config.get("model", "qwen-1.5-embeddings")
        self.dimensions: int | None = config.get("dimensions")
        self._endpoint: str = "https://qwenapi.cn/v1/embeddings"

        if not self.api_key:
            raise ValueError("api_key is required for QwenEmbedding")

    def _request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        resp = requests.post(self._endpoint, headers=headers,
                             data=json.dumps(payload))
        resp.raise_for_status()
        return resp.json()

    def embed(self, text: Union[str, List[str]]) -> List[List[float]]:
        """
        获取文本的向量表示

        :param text: 单个文本字符串或文本列表
        :return: 向量列表
        """
        if isinstance(text, str):
            inputs = [text]
        else:
            inputs = text

        payload = {"model": self.model, "input": inputs}
        result = self._request(payload)

        embeddings = [item["embedding"] for item in result.get("data", [])]

        if not embeddings:
            raise RuntimeError("No embeddings returned from Qwen API")

        # 记录维度
        if self.dimensions is None:
            self.dimensions = len(embeddings[0])

        return embeddings

    def encode(self, text: Union[str, List[str]]) -> List[List[float]]:
        """
        兼容 sentence_transformers 的 encode 方法
        """
        return self.embed(text)

    def get_embedding_dim(self) -> int:
        """
        获取向量维度
        """
        if self.dimensions is None:
            raise RuntimeError(
                "Embedding dimension is unknown. Call embed() first.")
        return self.dimensions
