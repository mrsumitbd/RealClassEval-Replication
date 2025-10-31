
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
        self.q_values = {a: 0.0 for a in range(self.action_space.n)}
        self.action_counts = {a: 0 for a in range(self.action_space.n)}
        self.last_action = None

    def select_action(self, observation):
        '''
        Select an action based on the current observation.
        Uses simple epsilon-greedy strategy.
        '''
        if random.random() < self.epsilon:
            action = self.action_space.sample()
        else:
            max_q = max(self.q_values.values())
            best_actions = [a for a, q in self.q_values.items() if q == max_q]
            action = random.choice(best_actions)
        self.last_action = action
        return action

    def update(self, action, reward):
        if action is None:
            return
        self.action_counts[action] += 1
        alpha = 1.0 / self.action_counts[action]
        self.q_values[action] += alpha * (reward - self.q_values[action])
