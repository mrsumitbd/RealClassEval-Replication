from typing import Union, List, Optional
import requests
import math


class QwenEmbedding:
    '''千问模型的 Embedding 实现'''

    def __init__(self, config=None):
        '''
        初始化千问 Embedding
        :param config: 配置字典，包含 api_key, model, dimensions 等参数
        '''
        config = config or {}
        self.api_key: str = config.get('api_key') or config.get('apiKey') or ''
        if not self.api_key:
            raise ValueError('api_key is required')
        self.model: str = config.get('model', 'text-embedding-v2')
        self.base_url: str = config.get(
            'base_url', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
        self.timeout: Optional[float] = config.get('timeout', 30)
        self._dimension: Optional[int] = config.get('dimensions')
        self.normalize: bool = bool(config.get('normalize', False))
        self.proxies = config.get('proxies')

    def embed(self, text: Union[str, List[str]]) -> List[List[float]]:
        '''
        获取文本的向量表示
        :param text: 单个文本字符串或文本列表
        :return: 向量列表
        '''
        if isinstance(text, str):
            inputs = [text]
        elif isinstance(text, list):
            inputs = [t if isinstance(t, str) else str(t) for t in text]
        else:
            raise TypeError('text must be str or List[str]')

        payload = {
            'model': self.model,
            'input': inputs
        }
        if self._dimension:
            payload['dimensions'] = int(self._dimension)

        url = f'{self.base_url.rstrip("/")}/embeddings'
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        resp = requests.post(url, headers=headers, json=payload,
                             timeout=self.timeout, proxies=self.proxies)
        if resp.status_code >= 400:
            try:
                err = resp.json()
            except Exception:
                err = {'message': resp.text}
            message = err.get('error', {}).get(
                'message') if isinstance(err, dict) else None
            message = message or err.get(
                'message') if isinstance(err, dict) else message
            raise RuntimeError(
                f'Embedding request failed: HTTP {resp.status_code}, {message}')

        data = resp.json()
        if 'data' not in data or not isinstance(data['data'], list):
            raise RuntimeError('Invalid response format: missing data field')

        # Ensure order by index
        items = sorted(data['data'], key=lambda x: x.get('index', 0))
        embeddings: List[List[float]] = [
            item.get('embedding', []) for item in items]

        if not embeddings or not isinstance(embeddings[0], list):
            raise RuntimeError(
                'Invalid response format: missing embedding vectors')

        if self._dimension is None and embeddings and embeddings[0]:
            self._dimension = len(embeddings[0])

        if self.normalize:
            embeddings = [self._l2_normalize(vec) for vec in embeddings]

        return embeddings

    def encode(self, text: Union[str, List[str]]) -> List[List[float]]:
        '''
        兼容 sentence_transformers 的 encode 方法
        '''
        return self.embed(text)

    def get_embedding_dim(self) -> int:
        '''
        获取向量维度
        '''
        if self._dimension is None:
            raise ValueError(
                'Embedding dimension is unknown. Call embed() once or set "dimensions" in config.')
        return int(self._dimension)

    @staticmethod
    def _l2_normalize(vec: List[float]) -> List[float]:
        norm = math.sqrt(sum((v * v for v in vec))) or 1.0
        return [v / norm for v in vec]
