from typing import Union, List, Optional, Dict, Any
import os
import json
import requests


class QwenEmbedding:
    '''千问模型的 Embedding 实现'''

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        '''
        初始化千问 Embedding
        :param config: 配置字典，包含 api_key, model, dimensions 等参数
        '''
        cfg = config or {}
        self.api_key: Optional[str] = cfg.get('api_key') or os.getenv(
            'DASHSCOPE_API_KEY') or os.getenv('QWEN_API_KEY') or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError(
                'QwenEmbedding requires an api_key via config["api_key"] or environment variable (DASHSCOPE_API_KEY/QWEN_API_KEY/OPENAI_API_KEY)')
        self.model: str = cfg.get('model') or 'text-embedding-v2'
        self.base_url: str = (cfg.get(
            'base_url') or 'https://dashscope.aliyuncs.com/compatible-mode/v1').rstrip('/')
        self._dimensions: Optional[int] = cfg.get('dimensions')
        self._timeout: float = float(cfg.get('timeout', 30))
        self._session = requests.Session()
        self._session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        })

    def embed(self, text: Union[str, List[str]]) -> List[List[float]]:
        '''
        获取文本的向量表示
        :param text: 单个文本字符串或文本列表
        :return: 向量列表
        '''
        if isinstance(text, str):
            inputs = [text]
        elif isinstance(text, list):
            if not all(isinstance(t, str) for t in text):
                raise TypeError('All items in the input list must be strings')
            inputs = text
        else:
            raise TypeError('text must be a string or a list of strings')

        if len(inputs) == 0:
            return []

        payload: Dict[str, Any] = {
            'model': self.model,
            'input': inputs,
        }
        if self._dimensions is not None:
            payload['dimensions'] = self._dimensions

        url = f'{self.base_url}/embeddings'
        resp = self._session.post(
            url, data=json.dumps(payload), timeout=self._timeout)
        if resp.status_code != 200:
            try:
                err = resp.json()
            except Exception:
                err = {'error': resp.text}
            raise RuntimeError(
                f'Embedding request failed: HTTP {resp.status_code}, {err}')

        data = resp.json()
        if 'data' not in data or not isinstance(data['data'], list):
            raise RuntimeError(f'Unexpected embedding response format: {data}')

        embeddings: List[List[float]] = []
        for item in data['data']:
            emb = item.get('embedding')
            if emb is None or not isinstance(emb, list):
                raise RuntimeError(f'Malformed embedding item: {item}')
            embeddings.append(emb)

        if self._dimensions is None and embeddings:
            self._dimensions = len(embeddings[0])

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
        if self._dimensions is not None:
            return self._dimensions
        raise ValueError(
            'Embedding dimension is unknown. Generate an embedding first or specify config["dimensions"] in initialization.')
