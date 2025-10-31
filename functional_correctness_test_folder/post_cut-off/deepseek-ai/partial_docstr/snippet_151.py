
import random


class SimpleAgent:
    '''
    A simple agent that selects actions for the TutorEnv.
    This is a placeholder for an actual Atropos policy.
    '''

    def __init__(self, action_space):
        '''Initialize with the action space of the environment.'''
        self.action_space = action_space
        self.epsilon = 0.1  # Exploration rate

    def select_action(self, observation):
        '''
        Select an action based on the current observation.
        Uses simple epsilon-greedy strategy.
        '''
        if random.random() < self.epsilon:
            return self.action_space.sample()  # Explore
        else:
            # Greedy action (placeholder: select first action)
            return 0  # Replace with actual policy logic

    def update(self, action, reward):
        '''Update the agent's policy based on the action and reward.'''
        pass  # No learning in this simple agent
