import numpy as np
import random

class SimpleAgent:
    """
    A simple agent that selects actions for the TutorEnv.
    This is a placeholder for an actual Atropos policy.
    """

    def __init__(self, action_space):
        """Initialize with the action space of the environment."""
        self.action_space = action_space
        self.last_rewards = []
        self.action_values = np.ones(action_space.n) * 0.5

    def select_action(self, observation):
        """
        Select an action based on the current observation.
        Uses simple epsilon-greedy strategy.
        """
        epsilon = 0.2
        if random.random() < epsilon:
            return self.action_space.sample()
        else:
            return np.argmax(self.action_values)

    def update(self, action, reward):
        """Update action values based on reward."""
        learning_rate = 0.1
        self.action_values[action] = (1 - learning_rate) * self.action_values[action] + learning_rate * reward
        self.last_rewards.append(reward)