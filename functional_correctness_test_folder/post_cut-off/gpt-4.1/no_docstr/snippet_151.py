
import random


class SimpleAgent:

    def __init__(self, action_space):
        self.action_space = action_space
        self.last_action = None
        self.last_reward = None

    def select_action(self, observation):
        action = random.choice(self.action_space)
        self.last_action = action
        return action

    def update(self, action, reward):
        self.last_action = action
        self.last_reward = reward
