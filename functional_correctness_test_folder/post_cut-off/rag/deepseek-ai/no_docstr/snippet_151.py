
import numpy as np


class SimpleAgent:
    '''
    A simple agent that selects actions for the TutorEnv.
    This is a placeholder for an actual Atropos policy.
    '''

    def __init__(self, action_space):
        '''Initialize with the action space of the environment.'''
        self.action_space = action_space
        self.action_values = np.zeros(action_space.n)
        self.action_counts = np.zeros(action_space.n)
        self.epsilon = 0.1  # Exploration rate

    def select_action(self, observation):
        '''
        Select an action based on the current observation.
        Uses simple epsilon-greedy strategy.
        '''
        if np.random.random() < self.epsilon:
            return self.action_space.sample()  # Explore
        else:
            return np.argmax(self.action_values)  # Exploit

    def update(self, action, reward):
        '''Update action values based on reward.'''
        self.action_counts[action] += 1
        # Incremental update rule (Q = Q + (1/N)(reward - Q))
        self.action_values[action] += (reward - self.action_values[action]
                                       ) / self.action_counts[action]
