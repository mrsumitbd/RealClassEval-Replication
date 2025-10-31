
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
        self.config = config or {}
        self.api_key = self.config.get("api_key")
        self.model = self.config.get("model", "qwen-1.5-emb")
        self.dimensions = self.config.get("dimensions")
        self._endpoint = "https://qwenapi.cn/v1/embeddings"

        if not self.api_key:
            raise ValueError("api_key must be provided in config")

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

        embeddings = []
        for item in result.get("data", []):
            emb = item.get("embedding")
            if emb is None:
                raise RuntimeError("Missing embedding in response")
            embeddings.append(emb)

        # 如果输入是单个字符串，返回单个向量
        if isinstance(text, str):
            return [embeddings[0]]
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
        if self.dimensions is not None:
            return self.dimensions

        # 尝试从一次请求中推断维度
        dummy = "test"
        try:
            emb = self.embed(dummy)[0]
            return len(emb)
        except Exception:
            raise RuntimeError("Unable to determine embedding dimension")
