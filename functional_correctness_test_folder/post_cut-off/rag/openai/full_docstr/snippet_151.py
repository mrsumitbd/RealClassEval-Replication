
import numpy as np
import gym


class SimpleAgent:
    """
    A simple agent that selects actions for the TutorEnv.
    This is a placeholder for an actual Atropos policy.
    """

    def __init__(self, action_space):
        """Initialize with the action space of the environment."""
        self.action_space = action_space
        # Epsilon-greedy parameters
        self.epsilon = 0.1
        self.alpha = 0.1  # learning rate

        # Initialise Q-values for discrete action spaces
        if isinstance(action_space, gym.spaces.Discrete):
            self.q_values = np.zeros(action_space.n, dtype=np.float32)
        else:
            # For non-discrete spaces we simply return zeros
            self.q_values = None

    def select_action(self, observation):
        """
        Select an action based on the current observation.
        Uses simple epsilon-greedy strategy.
        """
        if self.q_values is None:
            # Non-discrete action space: return zeros of the correct shape
            if isinstance(self.action_space, gym.spaces.Box):
                return np.zeros_like(self.action_space.sample())
            else:
                # Fallback: sample from the action space
                return self.action_space.sample()

        if np.random.rand() < self.epsilon:
            return self.action_space.sample()
        else:
            # Greedy action
            return int(np.argmax(self.q_values))

    def update(self, action, reward):
        """Update action values based on reward."""
        if self.q_values is None:
            return
        # Simple Q‑learning update with no discount
        self.q_values[action] += self.alpha * (reward - self.q_values[action])
