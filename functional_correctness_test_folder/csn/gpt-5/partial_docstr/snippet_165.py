class Inputs:

    def __init__(self, gaia):
        '''Initialize.'''
        self.gaia = gaia
        self.chats = []
        self.actions = []

    def add_chat(self, chat):
        if chat is None:
            raise ValueError("chat cannot be None")
        self.chats.append(chat)
        return self

    def add_action(self, action):
        if action is None:
            raise ValueError("action cannot be None")
        self.actions.append(action)
        return self
