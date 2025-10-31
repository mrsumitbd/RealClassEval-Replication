class Inputs:
    def __init__(self, gaia):
        self.gaia = gaia
        self.chats = []
        self.actions = []

    def add_chat(self, chat):
        self.chats.append(chat)

    def add_action(self, action):
        self.actions.append(action)
