from typing import Optional, Union
from openai import OpenAI

class OpenAICompatibleProvider:

    def __init__(self, api_key: str, base_url: str, model: Union[str, None]=None):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    @property
    def get_client(self):
        return self.client

    @staticmethod
    def test_connection(api_key: str, base_url: str) -> bool:
        try:
            client = OpenAI(api_key=api_key, base_url=base_url)
            model = client.models.list()
            logging.info('连通性测试成功')
            return True
        except Exception as e:
            logging.info(f'连通性测试失败：{e}')
            return False