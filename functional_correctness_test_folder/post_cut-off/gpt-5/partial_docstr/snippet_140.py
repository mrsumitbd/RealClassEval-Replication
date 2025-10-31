from typing import Union, List, Optional, Dict, Any
import hashlib
import math
import random


class QwenEmbedding:
    '''千问模型的 Embedding 实现'''

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        '''
        初始化千问 Embedding
        :param config: 配置字典，包含 api_key, model, dimensions 等参数
        '''
        cfg = config or {}
        self.api_key: Optional[str] = cfg.get('api_key')
        self.model: str = cfg.get('model', 'qwen2-embedding')
        self.dimensions: int = int(cfg.get('dimensions', 1536))
        self.normalize: bool = bool(cfg.get('normalize', True))

        if self.dimensions <= 0:
            raise ValueError('dimensions 必须为正整数')

    def embed(self, text: Union[str, List[str]]) -> List[List[float]]:
        '''
        获取文本的向量表示
        :param text: 单个文本字符串或文本列表
        :return: 向量列表
        '''
        texts = [text] if isinstance(text, str) else list(text)
        vectors: List[List[float]] = []
        for t in texts:
            if not isinstance(t, str):
                raise TypeError('text 内元素必须为字符串')
            vec = self._deterministic_embed(t)
            vectors.append(vec)
        return vectors

    def encode(self, text: Union[str, List[str]]) -> List[List[float]]:
        '''
        兼容 sentence_transformers 的 encode 方法
        '''
        return self.embed(text)

    def get_embedding_dim(self) -> int:
        return self.dimensions

    def _deterministic_embed(self, text: str) -> List[float]:
        seed_material = f'{self.model}::{self.dimensions}::{text}'.encode(
            'utf-8')
        seed = int.from_bytes(hashlib.sha256(
            seed_material).digest()[:8], 'big')
        rng = random.Random(seed)
        vec = [rng.uniform(-1.0, 1.0) for _ in range(self.dimensions)]
        if self.normalize:
            norm = math.sqrt(sum(v * v for v in vec)) or 1.0
            vec = [v / norm for v in vec]
        return vec
