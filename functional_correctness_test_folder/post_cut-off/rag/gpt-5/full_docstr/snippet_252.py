from typing import Callable


class BasePlugin:
    '''
    插件基类。插件需继承此类，并实现 register_frontend, register_backend 方法。
    '''

    def register_frontend(self, register_func: Callable[[str, str], None]) -> None:
        '''
        注册前端内容。register_func(路由, 文件路径)
        '''
        if not callable(register_func):
            raise TypeError('register_func must be callable')
        raise NotImplementedError(
            f'{self.__class__.__name__}.register_frontend must be implemented in subclass')

    def register_backend(self, app) -> None:
        '''
        注册后端路由。app为后端框架实例（如Flask/FastAPI等）
        '''
        if app is None:
            raise ValueError('app cannot be None')
        raise NotImplementedError(
            f'{self.__class__.__name__}.register_backend must be implemented in subclass')
