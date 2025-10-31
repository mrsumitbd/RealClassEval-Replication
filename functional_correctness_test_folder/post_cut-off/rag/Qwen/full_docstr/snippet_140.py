
from typing import Union, List
import requests


class QwenEmbedding:
    '''千问模型的 Embedding 实现'''

    def __init__(self, config=None):
        '''
        初始化千问 Embedding
        :param config: 配置字典，包含 api_key, model, dimensions 等参数
        '''
        self.config = config or {}
        self.api_key = self.config.get('api_key', '')
        self.model = self.config.get('model', 'default_model')
        self.dimensions = self.config.get('dimensions', 768)
        self.api_url = self.config.get(
            'api_url', 'https://api.qwen.com/v1/embeddings')

    def embed(self, text: Union[str, List[str]]) -> List[List[float]]:
        '''
        获取文本的向量表示
        :param text: 单个文本字符串或文本列表
        :return: 向量列表
        '''
        if isinstance(text, str):
            text = [text]
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            'model': self.model,
            'input': text
        }
        response = requests.post(self.api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json().get('data', [])

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
