from typing import Union, List, Optional
import os
import requests


class QwenEmbedding:
    '''千问模型的 Embedding 实现'''

    def __init__(self, config=None):
        '''
        初始化千问 Embedding
        :param config: 配置字典，包含 api_key, model, dimensions 等参数
        '''
        cfg = config or {}
        self.api_key: str = cfg.get('api_key') or os.getenv(
            'DASHSCOPE_API_KEY') or os.getenv('QWEN_API_KEY') or ''
        self.model: str = cfg.get('model', 'text-embedding-v3')
        self.dimensions: Optional[int] = cfg.get('dimensions')
        self.base_url: str = cfg.get(
            'base_url', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
        self.timeout: int = int(cfg.get('timeout', 30))
        self.batch_size: int = int(cfg.get('batch_size', 128))
        self._embedding_dim: Optional[int] = None

        self._session = requests.Session()
        if self.api_key:
            self._session.headers.update(
                {'Authorization': f'Bearer {self.api_key}'})
        self._session.headers.update({'Content-Type': 'application/json'})

    def embed(self, text: Union[str, List[str]]) -> List[List[float]]:
        '''
        获取文本的向量表示
        :param text: 单个文本字符串或文本列表
        :return: 向量列表
        '''
        if text is None:
            return []
        inputs = [text] if isinstance(text, str) else list(text)
        if not inputs:
            return []

        url = f'{self.base_url}/embeddings'
        all_embeddings: List[List[float]] = []
        for i in range(0, len(inputs), self.batch_size):
            chunk = inputs[i:i + self.batch_size]
            payload = {'model': self.model, 'input': chunk}
            if self.dimensions:
                payload['dimensions'] = self.dimensions
            resp = self._session.post(url, json=payload, timeout=self.timeout)
            if resp.status_code != 200:
                try:
                    detail = resp.json()
                except Exception:
                    detail = resp.text
                raise RuntimeError(
                    f'Qwen embedding request failed: {resp.status_code}, {detail}')
            data = resp.json()
            if 'data' not in data:
                raise RuntimeError(f'Invalid response: {data}')
            embeddings = [item['embedding'] for item in data['data']]
            all_embeddings.extend(embeddings)
            if not self._embedding_dim and embeddings:
                self._embedding_dim = len(embeddings[0])
        return all_embeddings

    def encode(self, text: Union[str, List[str]]):
        '''
        兼容 sentence_transformers 的 encode 方法
        '''
        vectors = self.embed(text)
        if isinstance(text, str):
            return vectors[0] if vectors else []
        return vectors

    def get_embedding_dim(self) -> int:
        '''
        获取向量维度
        '''
        if self.dimensions:
            return int(self.dimensions)
        if self._embedding_dim:
            return int(self._embedding_dim)
        vecs = self.embed('dimension_probe')
        if vecs:
            self._embedding_dim = len(vecs[0])
            return self._embedding_dim
        raise RuntimeError('Unable to determine embedding dimension.')
