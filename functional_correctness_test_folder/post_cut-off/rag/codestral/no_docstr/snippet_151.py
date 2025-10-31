
class SimpleAgent:
    '''
    A simple agent that selects actions for the TutorEnv.
    This is a placeholder for an actual Atropos policy.
    '''

    def __init__(self, action_space):
        '''Initialize with the action space of the environment.'''
        self.action_space = action_space
        self.epsilon = 0.1  # Exploration rate
        self.action_values = {action: 0.0 for action in range(
            action_space.n)}  # Initialize action values to 0
        # Count how many times each action has been taken
        self.action_counts = {action: 0 for action in range(action_space.n)}

    def select_action(self, observation):
        '''
        Select an action based on the current observation.
        Uses simple epsilon-greedy strategy.
        '''
        if np.random.rand() < self.epsilon:
            # Explore: select a random action
            return self.action_space.sample()
        else:
            # Exploit: select the action with the highest value
            return max(self.action_values.items(), key=lambda x: x[1])[0]

    def update(self, action, reward):
        '''Update action values based on reward.'''
        self.action_counts[action] += 1
        # Simple average update rule
        self.action_values[action] += (reward - self.action_values[action]
                                       ) / self.action_counts[action]
