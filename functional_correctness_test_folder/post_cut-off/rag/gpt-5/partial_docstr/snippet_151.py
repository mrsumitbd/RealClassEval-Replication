import numpy as np


class SimpleAgent:
    '''
    A simple agent that selects actions for the TutorEnv.
    This is a placeholder for an actual Atropos policy.
    '''

    def __init__(self, action_space):
        '''Initialize with the action space of the environment.'''
        self.action_space = action_space
        self.epsilon = 0.1
        self.num_actions = getattr(action_space, 'n', None)
        if self.num_actions is not None:
            self.q_values = np.zeros(self.num_actions, dtype=np.float64)
            self.counts = np.zeros(self.num_actions, dtype=np.int64)
        else:
            self.q_values = None
            self.counts = None

    def select_action(self, observation):
        '''
        Select an action based on the current observation.
        Uses simple epsilon-greedy strategy.
        '''
        if self.num_actions is None:
            return self.action_space.sample()
        if np.random.rand() < self.epsilon:
            return self.action_space.sample()
        max_val = np.max(self.q_values)
        best_actions = np.flatnonzero(self.q_values == max_val)
        return int(np.random.choice(best_actions))

    def update(self, action, reward):
        '''Update action values based on reward.'''
        if self.num_actions is None:
            return
        a = int(action)
        self.counts[a] += 1
        alpha = 1.0 / self.counts[a]
        self.q_values[a] += alpha * (float(reward) - self.q_values[a])
