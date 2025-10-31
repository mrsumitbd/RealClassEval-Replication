
class BasePlugin:
    '''
    插件基类。插件需继承此类，并实现 register_frontend, register_backend 方法。
    '''

    def register_frontend(self, register_func: Callable[[str, str], None]):
        '''
        注册前端内容。register_func(路由, 文件路径)
        '''
        pass

    def register_backend(self, app):
        '''
        注册后端路由。app为后端框架实例（如Flask/FastAPI等）
        '''
        pass
