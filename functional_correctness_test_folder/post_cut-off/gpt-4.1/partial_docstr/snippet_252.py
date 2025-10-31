
from typing import Callable


class BasePlugin:
    '''
    插件基类。插件需继承此类，并实现 register_frontend, register_backend 方法。
    '''

    def register_frontend(self, register_func: Callable[[str, str], None]):
        raise NotImplementedError("register_frontend 方法需要在子类中实现。")

    def register_backend(self, app):
        '''
        注册后端路由。app为后端框架实例（如Flask/FastAPI等）
        '''
        raise NotImplementedError("register_backend 方法需要在子类中实现。")
