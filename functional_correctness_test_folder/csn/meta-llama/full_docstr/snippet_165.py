
class Inputs:
    '''Normalize player inputs.'''

    def __init__(self, gaia):
        '''Initialize.'''
        self.gaia = gaia
        self.chat_inputs = []
        self.action_inputs = []

    def add_chat(self, chat):
        '''Add chat input.'''
        self.chat_inputs.append(chat)

    def add_action(self, action):
        '''Add action input.'''
        self.action_inputs.append(action)
