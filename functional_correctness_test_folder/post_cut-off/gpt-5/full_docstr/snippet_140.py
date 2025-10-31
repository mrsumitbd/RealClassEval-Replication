from typing import List, Union, Optional, Dict
import hashlib
import math
import random


class QwenEmbedding:
    '''千问模型的 Embedding 实现'''

    def __init__(self, config: Optional[Dict] = None):
        '''
        初始化千问 Embedding
        :param config: 配置字典，包含 api_key, model, dimensions 等参数
        '''
        self.config = config or {}
        self.api_key: Optional[str] = self.config.get("api_key")
        self.model: str = self.config.get("model", "qwen2-embedding")
        self.dimensions: int = int(self.config.get("dimensions", 768))
        if self.dimensions <= 0:
            raise ValueError("dimensions 必须为正整数")

    def _deterministic_vector(self, text: str) -> List[float]:
        seed_material = f"{self.model}::{text}".encode("utf-8")
        seed_int = int.from_bytes(
            hashlib.sha256(seed_material).digest(), "big")
        rng = random.Random(seed_int)
        vec = [rng.uniform(-1.0, 1.0) for _ in range(self.dimensions)]
        # L2 归一化
        norm = math.sqrt(sum(x * x for x in vec)) or 1.0
        return [x / norm for x in vec]

    def embed(self, text: Union[str, List[str]]) -> List[List[float]]:
        '''
        获取文本的向量表示
        :param text: 单个文本字符串或文本列表
        :return: 向量列表
        '''
        if isinstance(text, str):
            items = [text]
        elif isinstance(text, list):
            items = ["" if t is None else str(t) for t in text]
        else:
            raise TypeError("text 必须为 str 或 List[str]")

        return [self._deterministic_vector(t) for t in items]

    def encode(self, text: Union[str, List[str]]) -> List[List[float]]:
        '''
        兼容 sentence_transformers 的 encode 方法
        '''
        return self.embed(text)

    def get_embedding_dim(self) -> int:
        '''
        获取向量维度
        '''
        return self.dimensions
