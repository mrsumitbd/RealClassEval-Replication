
import random


class SimpleAgent:
    '''
    A simple agent that selects actions for the TutorEnv.
    This is a placeholder for an actual Atropos policy.
    '''

    def __init__(self, action_space, epsilon=0.1):
        '''Initialize with the action space of the environment.'''
        self.action_space = action_space
        self.epsilon = epsilon
        self.q_values = {action: 0 for action in action_space}

    def select_action(self, observation):
        '''
        Select an action based on the current observation.
        Uses simple epsilon-greedy strategy.
        '''
        if random.random() < self.epsilon:
            return random.choice(self.action_space)
        else:
            return max(self.q_values, key=self.q_values.get)

    def update(self, action, reward):
        self.q_values[action] += reward
