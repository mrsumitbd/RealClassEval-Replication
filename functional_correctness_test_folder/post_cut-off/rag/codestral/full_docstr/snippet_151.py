
class SimpleAgent:
    '''
    A simple agent that selects actions for the TutorEnv.
    This is a placeholder for an actual Atropos policy.
    '''

    def __init__(self, action_space):
        '''Initialize with the action space of the environment.'''
        self.action_space = action_space
        self.epsilon = 0.1  # Exploration rate
        self.action_values = np.zeros(
            action_space.n)  # Initialize action values
        # Count of times each action was taken
        self.action_counts = np.zeros(action_space.n)

    def select_action(self, observation):
        '''
        Select an action based on the current observation.
        Uses simple epsilon-greedy strategy.
        '''
        if np.random.rand() < self.epsilon:
            return self.action_space.sample()  # Explore: random action
        else:
            return np.argmax(self.action_values)  # Exploit: best action

    def update(self, action, reward):
        '''Update action values based on reward.'''
        self.action_counts[action] += 1
        # Incremental update of action value
        self.action_values[action] += (reward - self.action_values[action]
                                       ) / self.action_counts[action]
