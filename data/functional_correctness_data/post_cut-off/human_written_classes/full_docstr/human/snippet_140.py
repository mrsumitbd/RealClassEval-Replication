import os
from openai import OpenAI
from typing import List, Union

class QwenEmbedding:
    """千问模型的 Embedding 实现"""

    def __init__(self, config=None):
        """
        初始化千问 Embedding
        :param config: 配置字典，包含 api_key, model, dimensions 等参数
        """
        self.config = config or {}
        api_key = self.config.get('api_key') or os.getenv('DASHSCOPE_API_KEY')
        if not api_key:
            raise ValueError('千问 API Key 未找到，请设置 DASHSCOPE_API_KEY 环境变量或在配置中提供 api_key')
        self.client = OpenAI(api_key=api_key, base_url=self.config.get('base_url', 'https://dashscope.aliyuncs.com/compatible-mode/v1'))
        self.model = self.config.get('model', 'text-embedding-v4')
        self.dimensions = self.config.get('dimensions', 1024)
        self.encoding_format = self.config.get('encoding_format', 'float')

    def embed(self, text: Union[str, List[str]]) -> List[List[float]]:
        """
        获取文本的向量表示
        :param text: 单个文本字符串或文本列表
        :return: 向量列表
        """
        if isinstance(text, str):
            input_texts = [text]
            is_single = True
        else:
            input_texts = text
            is_single = False
        try:
            response = self.client.embeddings.create(model=self.model, input=input_texts, dimensions=self.dimensions, encoding_format=self.encoding_format)
            embeddings = [data.embedding for data in response.data]
            if is_single:
                return embeddings[0]
            return embeddings
        except Exception as e:
            raise RuntimeError(f'千问 Embedding API 调用失败: {str(e)}')

    def encode(self, text: Union[str, List[str]]) -> List[List[float]]:
        """
        兼容 sentence_transformers 的 encode 方法
        """
        result = self.embed(text)
        if isinstance(text, str):
            return [result]
        return result

    def get_embedding_dim(self) -> int:
        """
        获取向量维度
        """
        return self.dimensions