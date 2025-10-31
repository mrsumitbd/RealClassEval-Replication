
class SimpleAgent:
    '''
    A simple agent that selects actions for the TutorEnv.
    This is a placeholder for an actual Atropos policy.
    '''

    def __init__(self, action_space):
        '''Initialize with the action space of the environment.'''
        self.action_space = action_space
        self.epsilon = 0.1  # Exploration rate
        self.q_values = {action: 0 for action in range(action_space.n)}
        self.last_action = None

    def select_action(self, observation):
        '''
        Select an action based on the current observation.
        Uses simple epsilon-greedy strategy.
        '''
        if np.random.random() < self.epsilon:
            action = self.action_space.sample()
        else:
            action = max(self.q_values, key=self.q_values.get)
        self.last_action = action
        return action

    def update(self, action, reward):
        if self.last_action is not None:
            self.q_values[self.last_action] += 0.1 * \
                (reward - self.q_values[self.last_action])
