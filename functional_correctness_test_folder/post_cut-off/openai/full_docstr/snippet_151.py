
import random


class SimpleAgent:
    '''
    A simple agent that selects actions for the TutorEnv.
    This is a placeholder for an actual Atropos policy.
    '''

    def __init__(self, action_space):
        '''Initialize with the action space of the environment.'''
        self.action_space = action_space
        # Assume discrete action space
        if hasattr(action_space, "n"):
            self.n_actions = action_space.n
        else:
            raise ValueError("Unsupported action space type")
        # Q-values for each action
        self.q_values = {a: 0.0 for a in range(self.n_actions)}
        # Hyperparameters
        self.epsilon = 0.1   # exploration rate
        self.alpha = 0.1     # learning rate

    def select_action(self, observation):
        '''
        Select an action based on the current observation.
        Uses simple epsilon-greedy strategy.
        '''
        if random.random() < self.epsilon:
            # Explore: random action
            return random.choice(list(self.q_values.keys()))
        else:
            # Exploit: best known action
            max_q = max(self.q_values.values())
            best_actions = [a for a, q in self.q_values.items() if q == max_q]
            return random.choice(best_actions)

    def update(self, action, reward):
        '''Update action values based on reward.'''
        # Simple TD(0) update
        current_q = self.q_values[action]
        self.q_values[action] = current_q + self.alpha * (reward - current_q)
