
import random


class SimpleAgent:

    def __init__(self, action_space):

        self.action_space = action_space

    def select_action(self, observation):

        return random.choice(self.action_space)

    def update(self, action, reward):

        pass
