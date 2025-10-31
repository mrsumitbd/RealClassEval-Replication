
class Inputs:

    def __init__(self, gaia):
        '''Initialize.'''
        self.gaia = gaia
        self.chats = []
        self.actions = []

    def add_chat(self, chat):
        '''Add a chat message.'''
        self.chats.append(chat)

    def add_action(self, action):
        '''Add an action.'''
        self.actions.append(action)
