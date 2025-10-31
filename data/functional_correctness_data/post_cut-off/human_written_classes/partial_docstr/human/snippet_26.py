import os
import time
from typing import Optional, Dict
import httpx

class ManageApiClient:
    _instance = None
    _client = None
    _secret = None

    def __new__(cls, config):
        """单例模式确保全局唯一实例，并支持传入配置参数"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._init_client(config)
        return cls._instance

    @classmethod
    def _init_client(cls, config):
        """初始化持久化连接池"""
        cls.config = config.get('manager-api')
        if not cls.config:
            raise Exception('manager-api配置错误')
        if not cls.config.get('url') or not cls.config.get('secret'):
            raise Exception('manager-api的url或secret配置错误')
        if '你' in cls.config.get('secret'):
            raise Exception('请先配置manager-api的secret')
        cls._secret = cls.config.get('secret')
        cls.max_retries = cls.config.get('max_retries', 6)
        cls.retry_delay = cls.config.get('retry_delay', 10)
        cls._client = httpx.Client(base_url=cls.config.get('url'), headers={'User-Agent': f'PythonClient/2.0 (PID:{os.getpid()})', 'Accept': 'application/json', 'Authorization': 'Bearer ' + cls._secret}, timeout=cls.config.get('timeout', 30))

    @classmethod
    def _request(cls, method: str, endpoint: str, **kwargs) -> Dict:
        """发送单次HTTP请求并处理响应"""
        endpoint = endpoint.lstrip('/')
        response = cls._client.request(method, endpoint, **kwargs)
        response.raise_for_status()
        result = response.json()
        if result.get('code') == 10041:
            raise DeviceNotFoundException(result.get('msg'))
        elif result.get('code') == 10042:
            raise DeviceBindException(result.get('msg'))
        elif result.get('code') != 0:
            raise Exception(f"API返回错误: {result.get('msg', '未知错误')}")
        return result.get('data') if result.get('code') == 0 else None

    @classmethod
    def _should_retry(cls, exception: Exception) -> bool:
        """判断异常是否应该重试"""
        if isinstance(exception, (httpx.ConnectError, httpx.TimeoutException, httpx.NetworkError)):
            return True
        if isinstance(exception, httpx.HTTPStatusError):
            status_code = exception.response.status_code
            return status_code in [408, 429, 500, 502, 503, 504]
        return False

    @classmethod
    def _execute_request(cls, method: str, endpoint: str, **kwargs) -> Dict:
        """带重试机制的请求执行器"""
        retry_count = 0
        while retry_count <= cls.max_retries:
            try:
                return cls._request(method, endpoint, **kwargs)
            except Exception as e:
                if retry_count < cls.max_retries and cls._should_retry(e):
                    retry_count += 1
                    print(f'{method} {endpoint} 请求失败，将在 {cls.retry_delay:.1f} 秒后进行第 {retry_count} 次重试')
                    time.sleep(cls.retry_delay)
                    continue
                else:
                    raise

    @classmethod
    def safe_close(cls):
        """安全关闭连接池"""
        if cls._client:
            cls._client.close()
            cls._instance = None