
from typing import Optional, Callable, Any, List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Protocol

    class PluginManager(Protocol):
        pass

    class AppContext(Protocol):
        pass


class PluginAPI:

    def __init__(self, plugin_name: str, plugin_manager: 'PluginManager', app_context: Optional['AppContext'] = None):
        self._plugin_name = plugin_name
        self._plugin_manager = plugin_manager
        self._app_context = app_context

    @property
    def app_context(self) -> 'AppContext':
        if self._app_context is None:
            raise RuntimeError(
                "Application context has not been set on this PluginAPI instance.")
        return self._app_context

    def __getattr__(self, name: str) -> Callable[..., Any]:
        def method(*args, **kwargs):
            return getattr(self._plugin_manager, name)(*args, **kwargs)
        return method

    def list_available_apis(self) -> List[Dict[str, Any]]:
        return []

    def listen_for_event(self, event_name: str, callback: Callable[..., None]):
        pass

    def send_event(self, event_name: str, *args: Any, **kwargs: Any):
        pass

    def get_plugin_html_pages(self) -> List[Dict[str, str]]:
        return []
