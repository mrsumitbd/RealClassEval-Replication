
from typing import Callable


class BasePlugin:
    '''
    插件基类。插件需继承此类，并实现 register_frontend, register_backend 方法。
    '''

    def register_frontend(self, register_func: Callable[[str, str], None]):
        # 实现前端注册逻辑
        register_func('frontend_route', 'frontend_view')

    def register_backend(self, app):
        '''
        注册后端路由。app为后端框架实例（如Flask/FastAPI等）
        '''
        # 实现后端注册逻辑
        @app.route('/backend_route')
        def backend_view():
            return 'Backend Response'
