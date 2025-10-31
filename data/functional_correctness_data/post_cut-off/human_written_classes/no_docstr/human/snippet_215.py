class PromptFormat:

    def __init__(self, user_name, bot_name):
        self.user_name = user_name
        self.bot_name = bot_name

    def default_system_prompt(self, think):
        raise NotImplementedError()

    def format(self, system_prompt, messages):
        raise NotImplementedError()

    def add_bos(self):
        raise NotImplementedError()

    def thinktag(self):
        return ('<think>', '</think>')