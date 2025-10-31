import random
import numpy as np


class SimpleAgent:
    '''
    A simple agent that selects actions for the TutorEnv.
    This is a placeholder for an actual Atropos policy.
    '''

    def __init__(self, action_space):
        '''Initialize with the action space of the environment.'''
        self.action_space = action_space

        if hasattr(action_space, 'n'):
            self.n_actions = int(action_space.n)
        elif hasattr(action_space, '__len__'):
            self.n_actions = int(len(action_space))
        else:
            raise ValueError(
                'Unsupported action_space: must have attribute "n" or be a sized container')

        self.q_values = np.zeros(self.n_actions, dtype=np.float32)
        self.action_counts = np.zeros(self.n_actions, dtype=np.int64)

        self.epsilon = 0.1
        self.min_epsilon = 0.01
        self.epsilon_decay = 0.999
        self.steps = 0
        self.last_action = None

    def _random_action(self):
        if hasattr(self.action_space, 'sample'):
            return self.action_space.sample()
        return random.randrange(self.n_actions)

    def select_action(self, observation):
        '''
        Select an action based on the current observation.
        Uses simple epsilon-greedy strategy.
        '''
        self.steps += 1
        if random.random() < self.epsilon:
            action = self._random_action()
        else:
            max_q = np.max(self.q_values)
            candidates = np.flatnonzero(self.q_values == max_q)
            action = int(np.random.choice(candidates))
        self.last_action = action
        # Decay epsilon
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)
        return action

    def update(self, action, reward):
        '''Update action values based on reward.'''
        if action is None:
            action = self.last_action
        if action is None:
            return
        a = int(action)
        self.action_counts[a] += 1
        # Incremental average update (bandit-style)
        alpha = 1.0 / float(self.action_counts[a])
        self.q_values[a] += alpha * (float(reward) - self.q_values[a])
