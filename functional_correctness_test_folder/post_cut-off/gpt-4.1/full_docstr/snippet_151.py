
import random
from collections import defaultdict


class SimpleAgent:
    '''
    A simple agent that selects actions for the TutorEnv.
    This is a placeholder for an actual Atropos policy.
    '''

    def __init__(self, action_space):
        '''Initialize with the action space of the environment.'''
        self.action_space = action_space
        self.epsilon = 0.1
        self.alpha = 0.5
        self.q_values = defaultdict(float)
        self.last_action = None
        self.last_observation = None

    def select_action(self, observation):
        '''
        Select an action based on the current observation.
        Uses simple epsilon-greedy strategy.
        '''
        if random.random() < self.epsilon:
            action = self.action_space.sample()
        else:
            actions = range(self.action_space.n)
            q_vals = [self.q_values[(observation, a)] for a in actions]
            max_q = max(q_vals)
            best_actions = [a for a, q in zip(actions, q_vals) if q == max_q]
            action = random.choice(best_actions)
        self.last_observation = observation
        self.last_action = action
        return action

    def update(self, action, reward):
        '''Update action values based on reward.'''
        if self.last_observation is not None and self.last_action is not None:
            key = (self.last_observation, self.last_action)
            old_q = self.q_values[key]
            self.q_values[key] = old_q + self.alpha * (reward - old_q)
