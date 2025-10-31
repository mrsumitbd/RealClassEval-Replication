
class Inputs:
    '''Normalize player inputs.'''

    def __init__(self, gaia):
        '''Initialize.'''
        self.gaia = gaia
        self.chats = []
        self.actions = []

    def add_chat(self, chat):
        '''Add chat input.'''
        self.chats.append(chat)

    def add_action(self, action):
        '''Add action input.'''
        self.actions.append(action)
