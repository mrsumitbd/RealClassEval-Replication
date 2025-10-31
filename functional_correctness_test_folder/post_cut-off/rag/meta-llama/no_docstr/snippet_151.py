
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
        self.epsilon = 0.1  # Probability of selecting a random action
        self.action_values = {action: 0.0 for action in range(action_space.n)}

    def select_action(self, observation):
        """
        Select an action based on the current observation.
        Uses simple epsilon-greedy strategy.
        """
        if random.random() < self.epsilon:
            return random.randint(0, self.action_space.n - 1)
        else:
            # Select the action with the highest value
            max_value = max(self.action_values.values())
            max_actions = [
                action for action, value in self.action_values.items() if value == max_value]
            return random.choice(max_actions)

    def update(self, action, reward):
        """Update action values based on reward."""
        # Simple update rule: move the action value towards the received reward
        self.action_values[action] += 0.1 * \
            (reward - self.action_values[action])
