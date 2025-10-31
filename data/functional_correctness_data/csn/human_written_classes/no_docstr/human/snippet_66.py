import json
from webview.util import DEFAULT_HTML, create_cookie, js_bridge_call, inject_pywebview

class JSBridge:

    def __init__(self, window, eval_events):
        self.results = {}
        self.window = window
        self.eval_events = eval_events

    def return_result(self, result, uid):
        self.results[uid] = json.loads(result) if result else None
        self.eval_events[uid].set()

    def call(self, func_name, param, value_id):
        js_bridge_call(self.window, func_name, json.loads(param), value_id)