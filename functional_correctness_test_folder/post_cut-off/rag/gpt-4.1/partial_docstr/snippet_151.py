import numpy as np


class SimpleAgent:
    '''
    A simple agent that selects actions for the TutorEnv.
    This is a placeholder for an actual Atropos policy.
    '''

    def __init__(self, action_space):
        '''Initialize with the action space of the environment.'''
        self.action_space = action_space
        self.n_actions = action_space.n if hasattr(
            action_space, 'n') else len(action_space)
        self.q_values = np.zeros(self.n_actions, dtype=np.float32)
        self.epsilon = 0.1
        self.alpha = 0.1
        self.last_action = None

    def select_action(self, observation):
        '''
        Select an action based on the current observation.
        Uses simple epsilon-greedy strategy.
        '''
        if np.random.rand() < self.epsilon:
            action = self.action_space.sample() if hasattr(
                self.action_space, 'sample') else np.random.randint(self.n_actions)
        else:
            action = int(np.argmax(self.q_values))
        self.last_action = action
        return action

    def update(self, action, reward):
        '''Update action values based on reward.'''
        if self.last_action is not None:
            self.q_values[self.last_action] += self.alpha * \
                (reward - self.q_values[self.last_action])
