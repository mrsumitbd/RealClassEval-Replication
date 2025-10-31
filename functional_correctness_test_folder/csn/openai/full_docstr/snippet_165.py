class Inputs:
    '''Normalize player inputs.'''

    def __init__(self, gaia):
        '''Initialize.'''
        self.gaia = gaia
        self._chats = []
        self._actions = []

    def add_chat(self, chat):
        '''Add chat input.'''
        if not isinstance(chat, str):
            raise TypeError("chat must be a string")
        # Basic normalization: strip whitespace and lower‑case
        normalized = chat.strip().lower()
        self._chats.append(normalized)

    def add_action(self, action):
        '''Add action input.'''
        if not isinstance(action, dict):
            raise TypeError("action must be a dict")
        # Store a shallow copy to avoid accidental mutation
        self._actions.append(action.copy())
        # Optionally forward to gaia if it has a handler
        if hasattr(self.gaia, "handle_action"):
            self.gaia.handle_action(action)
        return action
