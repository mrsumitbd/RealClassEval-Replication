
class SimpleAgent:

    def __init__(self, action_space):
        self.action_space = action_space

    def select_action(self, observation):
        return self.action_space.sample()

    def update(self, action, reward):
        pass
