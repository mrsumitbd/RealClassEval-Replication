class State:

    def __init__(self, name, bot):
        self.name = name
        self.bot = bot

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def check_transitions(self):
        pass

    def do_state_stuff(self):
        pass