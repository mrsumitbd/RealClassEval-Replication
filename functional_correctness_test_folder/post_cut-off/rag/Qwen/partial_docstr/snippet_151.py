
import random
import numpy as np


class SimpleAgent:
    '''
    A simple agent that selects actions for the TutorEnv.
    This is a placeholder for an actual Atropos policy.
    '''

    def __init__(self, action_space, epsilon=0.1, alpha=0.1, gamma=0.99):
        '''Initialize with the action space of the environment.'''
        self.action_space = action_space
        self.epsilon = epsilon  # Exploration rate
        self.alpha = alpha      # Learning rate
        self.gamma = gamma      # Discount factor
        self.q_values = {state: {action: 0.0 for action in action_space}
                         for state in self._get_all_states()}

    def _get_all_states(self):
        # Placeholder for getting all possible states. This should be replaced with actual state generation.
        # For demonstration, let's assume a simple discrete state space.
        return range(10)  # Example state space

    def select_action(self, observation):
        '''
        Select an action based on the current observation.
        Uses simple epsilon-greedy strategy.
        '''
        if random.random() < self.epsilon:
            return random.choice(self.action_space)
        else:
            state_q_values = self.q_values[observation]
            max_q = max(state_q_values.values())
            actions_with_max_q = [
                action for action, q_value in state_q_values.items() if q_value == max_q]
            return random.choice(actions_with_max_q)

    def update(self, state, action, reward, next_state):
        '''Update action values based on reward.'''
        best_next_action = self.select_action(next_state)
        td_target = reward + self.gamma * \
            self.q_values[next_state][best_next_action]
        td_error = td_target - self.q_values[state][action]
        self.q_values[state][action] += self.alpha * td_error
