
import os
from typing import List, Union, Dict, Any

try:
    import openai
except ImportError:
    openai = None  # pragma: no cover


class QwenEmbedding:
    """千问模型的 Embedding 实现"""

    def __init__(self, config: Dict[str, Any] | None = None):
        """
        初始化千问 Embedding

        :param config: 配置字典，包含 api_key, model, dimensions 等参数
        """
        if config is None:
            config = {}

        self.api_key: str | None = config.get(
            "api_key") or os.getenv("OPENAI_API_KEY")
        self.model: str = config.get("model", "qwen-1.5-7b-chat")
        self._dimensions: int | None = config.get("dimensions")

        if openai is None:
            raise ImportError("openai package is required for QwenEmbedding")

        if self.api_key:
            openai.api_key = self.api_key

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

        # 调用 OpenAI 的 embedding 接口
        response = openai.Embedding.create(
            input=texts,
            model=self.model,
        )

        embeddings = [data["embedding"] for data in response["data"]]
        # 缓存维度信息
        if self._dimensions is None and embeddings:
            self._dimensions = len(embeddings[0])

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
        if self._dimensions is not None:
            return self._dimensions

        # 尝试通过一次调用获取维度
        dummy = self.embed("test")
        if dummy:
            self._dimensions = len(dummy[0])
            return self._dimensions

        raise ValueError("Unable to determine embedding dimension")
