
import random
import numpy as np


class SimpleAgent:
    '''
    A simple agent that selects actions for the TutorEnv.
    This is a placeholder for an actual Atropos policy.
    '''

    def __init__(self, action_space, epsilon=0.1, alpha=0.1, gamma=0.99):
        '''Initialize with the action space of the environment.'''
        # Determine number of actions
        if hasattr(action_space, "n"):
            self.n_actions = action_space.n
        else:
            self.n_actions = len(action_space)
        self.action_space = action_space
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma

        # Q‑table: mapping from observation hash to Q‑values array
        self.q_table = {}

        # Store last state and action for learning
        self.last_obs = None
        self.last_action = None

    def select_action(self, observation):
        '''
        Select an action based on the current observation.
        Uses simple epsilon‑greedy strategy.
        '''
        # Store current observation for later update
        self.last_obs = observation

        # Epsilon‑greedy
        if random.random() < self.epsilon:
            # Random action
            action = self._random_action()
        else:
            # Greedy action
            q_vals = self._get_q_values(observation)
            action = int(np.argmax(q_vals))
        self.last_action = action
        return action

    def update(self, action, reward):
        '''
        Update Q‑values based on the taken action and received reward.
        '''
        if self.last_obs is None or self.last_action is None:
            return  # nothing to update

        # Get current Q‑value
        q_vals = self._get_q_values(self.last_obs)
        current_q = q_vals[self.last_action]

        # TD(0) update (no next‑state info)
        td_target = reward
        td_error = td_target - current_q
        q_vals[self.last_action] += self.alpha * td_error

        # Store updated Q‑values
        self.q_table[self._hash_obs(self.last_obs)] = q_vals

        # Reset last state/action
        self.last_obs = None
        self.last_action = None

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------
    def _random_action(self):
        if hasattr(self.action_space, "sample"):
            return self.action_space.sample()
        else:
            return random.choice(self.action_space)

    def _get_q_values(self, observation):
        key = self._hash_obs(observation)
        if key not in self.q_table:
            self.q_table[key] = np.zeros(self.n_actions, dtype=np.float32)
        return self.q_table[key]

    def _hash_obs(self, observation):
        try:
            return hash(observation)
        except TypeError:
            # Fallback for unhashable observations (e.g., lists, arrays)
            return hash(str(observation))
