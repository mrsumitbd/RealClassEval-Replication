from typing import Any, Callable, Dict, List, Optional
import inspect


class PluginAPI:

    def __init__(self, plugin_name: str, plugin_manager: 'PluginManager', app_context: Optional['AppContext']):
        self._plugin_name = plugin_name
        self._plugin_manager = plugin_manager
        self._app_context = app_context
        self._api_cache: Dict[str, Callable[..., Any]] = {}

    @property
    def app_context(self) -> 'AppContext':
        if self._app_context is None:
            raise RuntimeError(
                "Application context has not been set on this PluginAPI instance.")
        return self._app_context

    def __getattr__(self, name: str) -> Callable[..., Any]:
        if name in self.__dict__:
            return self.__dict__[name]  # safeguard

        if name in self._api_cache:
            return self._api_cache[name]

        apis: Dict[str, Callable[..., Any]] = {}
        if hasattr(self._plugin_manager, "get_registered_apis") and callable(getattr(self._plugin_manager, "get_registered_apis")):
            apis = self._plugin_manager.get_registered_apis() or {}
        elif hasattr(self._plugin_manager, "registered_apis"):
            apis = getattr(self._plugin_manager, "registered_apis") or {}

        if name in apis:
            func = apis[name]
            self._api_cache[name] = func
            return func

        raise AttributeError(f"'PluginAPI' object has no attribute '{name}'")

    def list_available_apis(self) -> List[Dict[str, Any]]:
        apis: Dict[str, Callable[..., Any]] = {}
        if hasattr(self._plugin_manager, "get_registered_apis") and callable(getattr(self._plugin_manager, "get_registered_apis")):
            apis = self._plugin_manager.get_registered_apis() or {}
        elif hasattr(self._plugin_manager, "registered_apis"):
            apis = getattr(self._plugin_manager, "registered_apis") or {}

        result: List[Dict[str, Any]] = []
        for name, func in apis.items():
            try:
                sig = str(inspect.signature(func))
            except (TypeError, ValueError):
                sig = "(...)"
            doc = inspect.getdoc(func) or ""
            result.append({
                "name": name,
                "signature": sig,
                "doc": doc,
                "callable": func,
            })
        return result

    def listen_for_event(self, event_name: str, callback: Callable[..., None]):
        if hasattr(self._plugin_manager, "listen_for_event") and callable(getattr(self._plugin_manager, "listen_for_event")):
            self._plugin_manager.listen_for_event(
                self._plugin_name, event_name, callback)
            return
        if hasattr(self._plugin_manager, "register_event_listener") and callable(getattr(self._plugin_manager, "register_event_listener")):
            self._plugin_manager.register_event_listener(
                self._plugin_name, event_name, callback)
            return
        raise NotImplementedError(
            "PluginManager does not support event listening registration.")

    def send_event(self, event_name: str, *args: Any, **kwargs: Any):
        if hasattr(self._plugin_manager, "send_event") and callable(getattr(self._plugin_manager, "send_event")):
            self._plugin_manager.send_event(
                self._plugin_name, event_name, *args, **kwargs)
            return
        if hasattr(self._plugin_manager, "trigger_event") and callable(getattr(self._plugin_manager, "trigger_event")):
            self._plugin_manager.trigger_event(
                self._plugin_name, event_name, *args, **kwargs)
            return
        raise NotImplementedError(
            "PluginManager does not support sending events.")

    def get_plugin_html_pages(self) -> List[Dict[str, str]]:
        pages: List[Dict[str, str]] = []

        ctx = self._app_context
        if ctx is not None:
            router = getattr(ctx, "router", None)
            if router is not None:
                if hasattr(router, "get_routes_by_tag") and callable(getattr(router, "get_routes_by_tag")):
                    routes = router.get_routes_by_tag("html") or []
                    for r in routes:
                        name = getattr(r, "name", None) or (
                            r.get("name") if isinstance(r, dict) else None)
                        path = getattr(r, "path", None) or (
                            r.get("path") if isinstance(r, dict) else None)
                        if name and path:
                            pages.append(
                                {"name": str(name), "path": str(path)})
                        continue
                elif hasattr(router, "list_routes") and callable(getattr(router, "list_routes")):
                    routes = router.list_routes() or []
                    for r in routes:
                        tags = getattr(r, "tags", None) or (
                            r.get("tags") if isinstance(r, dict) else None)
                        if tags and ("html" in tags or "HTML" in tags):
                            name = getattr(r, "name", None) or (
                                r.get("name") if isinstance(r, dict) else None)
                            path = getattr(r, "path", None) or (
                                r.get("path") if isinstance(r, dict) else None)
                            if name and path:
                                pages.append(
                                    {"name": str(name), "path": str(path)})

        if not pages and hasattr(self._plugin_manager, "get_plugin_routes") and callable(getattr(self._plugin_manager, "get_plugin_routes")):
            routes = self._plugin_manager.get_plugin_routes(
                self._plugin_name) or []
            for r in routes:
                tags = getattr(r, "tags", None) or (
                    r.get("tags") if isinstance(r, dict) else None)
                if tags and ("html" in tags or "HTML" in tags):
                    name = getattr(r, "name", None) or (
                        r.get("name") if isinstance(r, dict) else None)
                    path = getattr(r, "path", None) or (
                        r.get("path") if isinstance(r, dict) else None)
                    if name and path:
                        pages.append({"name": str(name), "path": str(path)})

        return pages
