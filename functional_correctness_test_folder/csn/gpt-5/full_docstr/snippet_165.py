class Inputs:
    '''Normalize player inputs.'''

    def __init__(self, gaia):
        '''Initialize.'''
        self.gaia = gaia
        self._events = []
        self._counter = 0
        from threading import Lock
        self._lock = Lock()

    def _next_id(self):
        with self._lock:
            self._counter += 1
            return self._counter

    def _timestamp(self):
        import time
        return time.time()

    def add_chat(self, chat):
        '''Add chat input.'''
        if not isinstance(chat, str):
            raise TypeError("chat must be a string")
        text = chat.strip()
        if not text:
            raise ValueError("chat cannot be empty")
        evt = {
            "id": self._next_id(),
            "ts": self._timestamp(),
            "type": "chat",
            "text": text,
        }
        with self._lock:
            self._events.append(evt)
        return evt

    def add_action(self, action):
        '''Add action input.'''
        name = None
        params = {}

        if isinstance(action, str):
            name = action.strip()
            if not name:
                raise ValueError("action name cannot be empty")
        elif isinstance(action, (tuple, list)) and len(action) == 2:
            name, params = action
        elif isinstance(action, dict):
            name = action.get("name") or action.get("action")
            if "params" in action and isinstance(action["params"], dict):
                params = dict(action["params"])
            else:
                # Infer params from remaining keys if provided inline
                params = {k: v for k, v in action.items(
                ) if k not in ("name", "action", "params")}
        else:
            raise TypeError(
                "action must be a string, (name, params) tuple, or dict")

        if not isinstance(name, str):
            raise TypeError("action name must be a string")
        name = name.strip()
        if not name:
            raise ValueError("action name cannot be empty")

        if params is None:
            params = {}
        if not isinstance(params, dict):
            raise TypeError("action params must be a dict")

        evt = {
            "id": self._next_id(),
            "ts": self._timestamp(),
            "type": "action",
            "name": name,
            "params": params,
        }
        with self._lock:
            self._events.append(evt)
        return evt
