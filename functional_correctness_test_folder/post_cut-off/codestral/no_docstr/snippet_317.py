
class WebProcessMixin:

    def start_web_ui_direct(self, app_context: AppContext, host: Optional[Union[str, List[str]]] = None, debug: bool = False, threads: Optional[int] = None) -> None:
        pass

    def get_web_ui_pid_path(self) -> str:
        pass

    def get_web_ui_expected_start_arg(self) -> List[str]:
        pass

    def get_web_ui_executable_path(self) -> str:
        pass
