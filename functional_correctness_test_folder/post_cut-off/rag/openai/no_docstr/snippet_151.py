class SimpleAgent:
    '''
    A simple agent that selects actions for the TutorEnv.
    This is a placeholder for an actual Atropos policy.
    '''

    def __init__(self, action_space):
        '''Initialize with the action space of the environment.'''
        # Assume a discrete action space
        if hasattr(action_space, 'n'):
            self.n_actions = action_space.n
        else:
            raise ValueError("Unsupported action space type")
        # Initialize Q-values for each action
        self.q_values = [0.0 for _ in range(self.n_actions)]
        # Hyper‑parameters
        self.epsilon = 0.1   # exploration rate
        self.alpha = 0.1     # learning rate

    def select_action(self, observation):
        '''
        Select an action based on the current observation.
        Uses simple epsilon‑greedy strategy.
        '''
        import random
        if random.random() < self.epsilon:
            # Explore: pick a random action
            return random.randint(0, self.n_actions - 1)
        else:
            # Exploit: pick the action with the highest Q‑value
            max_q = max(self.q_values)
            # In case of ties, pick randomly among best actions
            best_actions = [i for i, q in enumerate(
                self.q_values) if q == max_q]
            return random.choice(best_actions)

    def update(self, action, reward):
        '''Update action values based on reward.'''
        # Simple Q‑learning update: Q ← Q + α (r − Q)
        self.q_values[action] += self.alpha * (reward - self.q_values[action])
