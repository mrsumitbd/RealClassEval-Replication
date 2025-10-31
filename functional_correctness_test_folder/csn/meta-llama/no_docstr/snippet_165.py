
class Inputs:

    def __init__(self, gaia):
        """
        Initialize the Inputs class.

        Args:
            gaia: The gaia object associated with the inputs.
        """
        self.gaia = gaia
        self.chats = []
        self.actions = []

    def add_chat(self, chat):
        """
        Add a chat to the list of chats.

        Args:
            chat: The chat to be added.
        """
        self.chats.append(chat)

    def add_action(self, action):
        """
        Add an action to the list of actions.

        Args:
            action: The action to be added.
        """
        self.actions.append(action)
