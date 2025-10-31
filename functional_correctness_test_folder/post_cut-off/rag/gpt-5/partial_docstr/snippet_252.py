from abc import ABC, abstractmethod
from typing import Callable, Any


class BasePlugin(ABC):
    '''
    插件基类。插件需继承此类，并实现 register_frontend, register_backend 方法。
    '''

    @abstractmethod
    def register_frontend(self, register_func: Callable[[str, str], None]) -> None:
        '''
        注册前端内容。register_func(路由, 文件路径)
        '''
        raise NotImplementedError(
            'register_frontend must be implemented by the plugin subclass')

    @abstractmethod
    def register_backend(self, app: Any) -> None:
        '''
        注册后端路由。app为后端框架实例（如Flask/FastAPI等）
        '''
        raise NotImplementedError(
            'register_backend must be implemented by the plugin subclass')
