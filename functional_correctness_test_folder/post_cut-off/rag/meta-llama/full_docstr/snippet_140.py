
from typing import Union, List
import requests
import json


class QwenEmbedding:
    '''千问模型的 Embedding 实现'''

    def __init__(self, config=None):
        '''
        初始化千问 Embedding
        :param config: 配置字典，包含 api_key, model, dimensions 等参数
        '''
        self.config = config or {}
        self.api_key = self.config.get('api_key')
        self.model = self.config.get('model', 'text-embedding-v2')
        self.dimensions = self.config.get('dimensions')
        self.base_url = 'https://dashscope.aliyuncs.com/api/v1/services/embedding'

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

        data = {
            'model': self.model,
            'input': text
        }

        if self.dimensions:
            data['parameters'] = {'text_type': 'document',
                                  'dimensions': self.dimensions}

        response = requests.post(
            self.base_url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            result = response.json()
            embeddings = result['output']['embeddings']
            return [embedding['embedding'] for embedding in embeddings]
        else:
            raise Exception(f'Failed to get embeddings: {response.text}')

    def encode(self, text: Union[str, List[str]]) -> List[List[float]]:
        '''
        兼容 sentence_transformers 的 encode 方法
        '''
        return self.embed(text)

    def get_embedding_dim(self) -> int:
        '''
        获取向量维度
        '''
        if self.dimensions:
            return self.dimensions
        else:
            # 默认维度或通过其他方式获取维度
            # 这里假设我们可以通过一次请求获取维度
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            data = {
                'model': self.model,
                'input': ['test']
            }
            response = requests.post(
                self.base_url, headers=headers, data=json.dumps(data))
            if response.status_code == 200:
                result = response.json()
                embedding = result['output']['embeddings'][0]['embedding']
                return len(embedding)
            else:
                raise Exception(
                    f'Failed to get embedding dimension: {response.text}')
