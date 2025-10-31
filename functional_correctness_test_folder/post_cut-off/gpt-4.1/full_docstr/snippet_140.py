
from typing import Union, List
import requests


class QwenEmbedding:
    '''千问模型的 Embedding 实现'''

    def __init__(self, config=None):
        '''
        初始化千问 Embedding
        :param config: 配置字典，包含 api_key, model, dimensions 等参数
        '''
        if config is None:
            config = {}
        self.api_key = config.get('api_key', '')
        self.model = config.get('model', 'qwen-embedding')
        self.dimensions = config.get('dimensions', 1536)
        self.api_url = config.get(
            'api_url', 'https://dashscope.aliyuncs.com/api/v1/services/aigc/embedding/text-embedding')
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def embed(self, text: Union[str, List[str]]) -> List[List[float]]:
        '''
        获取文本的向量表示
        :param text: 单个文本字符串或文本列表
        :return: 向量列表
        '''
        if isinstance(text, str):
            texts = [text]
        else:
            texts = text

        payload = {
            "model": self.model,
            "input": texts
        }
        response = requests.post(
            self.api_url, headers=self.headers, json=payload)
        response.raise_for_status()
        data = response.json()
        # 兼容不同返回格式
        if 'output' in data and 'embeddings' in data['output']:
            embeddings = data['output']['embeddings']
        elif 'data' in data:
            embeddings = [item['embedding'] for item in data['data']]
        else:
            raise ValueError("Unexpected response format: {}".format(data))
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
        return self.dimensions
