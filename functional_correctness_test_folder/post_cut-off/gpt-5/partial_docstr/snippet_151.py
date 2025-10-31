import random


class SimpleAgent:
    '''
    A simple agent that selects actions for the TutorEnv.
    This is a placeholder for an actual Atropos policy.
    '''

    def __init__(self, action_space):
        '''Initialize with the action space of the environment.'''
        self.action_space = action_space
        self.epsilon = 0.1
        self.alpha = 0.1
        if hasattr(action_space, 'n'):
            self.n_actions = action_space.n
        elif hasattr(action_space, '__len__'):
            self.n_actions = len(action_space)
        else:
            raise ValueError(
                "Unsupported action_space: cannot determine number of actions.")
        self.q_values = [0.0] * self.n_actions
        self.counts = [0] * self.n_actions
        self._rng = random.Random()

    def select_action(self, observation):
        '''
        Select an action based on the current observation.
        Uses simple epsilon-greedy strategy.
        '''
        del observation
        if self._rng.random() < self.epsilon:
            # Explore
            if hasattr(self.action_space, 'sample'):
                return self.action_space.sample()
            return self._rng.randrange(self.n_actions)
        # Exploit
        max_q = max(self.q_values)
        best_actions = [i for i, q in enumerate(self.q_values) if q == max_q]
        action_index = self._rng.choice(best_actions)
        return action_index

    def update(self, action, reward):
        self.counts[action] += 1
        self.q_values[action] += self.alpha * (reward - self.q_values[action])
