
from abc import ABC, abstractmethod
from typing import Callable


class BasePlugin(ABC):
    """
    插件基类。插件需继承此类，并实现 register_frontend, register_backend 方法。
    """

    @abstractmethod
    def register_frontend(self, register_func: Callable[[str, str], None]) -> None:
        """
        注册前端资源。`register_func` 接收两个字符串参数，分别为资源路径和资源内容或路径。
        """
        pass

    @abstractmethod
    def register_backend(self, app) -> None:
        """
        注册后端路由。`app` 为后端框架实例（如 Flask/FastAPI 等）。
        """
        pass
