
import random


class SimpleAgent:
    '''
    A simple agent that selects actions for the TutorEnv.
    This is a placeholder for an actual Atropos policy.
    '''

    def __init__(self, action_space):
        '''Initialize with the action space of the environment.'''
        self.action_space = action_space
        self.epsilon = 0.1  # Exploration rate
        self.q_values = {action: 0 for action in action_space}

    def select_action(self, observation):
        '''
        Select an action based on the current observation.
        Uses simple epsilon-greedy strategy.
        '''
        if random.random() < self.epsilon:
            return random.choice(self.action_space)
        else:
            max_q_value = max(self.q_values.values())
            max_actions = [
                action for action, q_value in self.q_values.items() if q_value == max_q_value]
            return random.choice(max_actions)

    def update(self, action, reward):
        '''Update the Q-value of the taken action based on the received reward.'''
        learning_rate = 0.1
        self.q_values[action] += learning_rate * \
            (reward - self.q_values[action])
