class Inputs:

    def __init__(self, gaia):
        self.gaia = gaia
        self.chats = []
        self.actions = []

    def add_chat(self, chat):
        if chat is None:
            return self
        if isinstance(chat, (list, tuple)):
            self.chats.extend(chat)
        else:
            self.chats.append(chat)
        return self

    def add_action(self, action):
        if action is None:
            return self
        if isinstance(action, (list, tuple)):
            self.actions.extend(action)
        else:
            self.actions.append(action)
        return self
