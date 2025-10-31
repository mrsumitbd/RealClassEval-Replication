from module.webui.utils import Icon, WebIOTaskHandler, set_localstorage
from pywebio.session import defer_call, info, run_js

class Base:

    def __init__(self) -> None:
        self.alive = True
        self.visible = True
        self.is_mobile = info.user_agent.is_mobile
        self.task_handler = WebIOTaskHandler()
        defer_call(self.stop)

    def stop(self) -> None:
        self.alive = False
        self.task_handler.stop()