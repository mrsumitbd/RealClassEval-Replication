
class Inputs:
    '''Normalize player inputs.'''

    def __init__(self, gaia):
        '''Initialize.'''
        self.gaia = gaia
        self.chats = []
        self.actions = []

    def add_chat(self, chat):
        '''Add chat input.'''
        if isinstance(chat, str):
            chat = chat.strip()
            if chat:
                self.chats.append(chat)

    def add_action(self, action):
        '''Add action input.'''
        if action is not None:
            self.actions.append(action)
