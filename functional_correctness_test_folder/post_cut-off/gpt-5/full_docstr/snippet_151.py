class SimpleAgent:
    '''
    A simple agent that selects actions for the TutorEnv.
    This is a placeholder for an actual Atropos policy.
    '''

    def __init__(self, action_space, epsilon=0.1, alpha=None, epsilon_decay=None, min_epsilon=0.01, seed=None):
        '''Initialize with the action space of the environment.'''
        self.action_space = action_space
        self.epsilon = float(epsilon)
        self.alpha = None if alpha is None else float(alpha)
        self.epsilon_decay = float(
            epsilon_decay) if epsilon_decay is not None else None
        self.min_epsilon = float(min_epsilon)
        self.rng = __import__("numpy").random.default_rng(seed)

        self.n_actions = self._infer_n_actions(action_space)
        self.q_values = __import__("numpy").zeros(self.n_actions, dtype=float)
        self.action_counts = __import__(
            "numpy").zeros(self.n_actions, dtype=int)

    def select_action(self, observation):
        '''
        Select an action based on the current observation.
        Uses simple epsilon-greedy strategy.
        '''
        del observation  # unused in simple agent
        explore = self.rng.random() < self.epsilon
        if explore:
            action = self._random_action()
        else:
            # Break ties uniformly at random among argmax
            q = self.q_values
            max_q = q.max()
            candidates = __import__("numpy").flatnonzero(q == max_q)
            action = int(self.rng.choice(candidates))
        if self.epsilon_decay is not None and self.epsilon > self.min_epsilon:
            self.epsilon = max(
                self.min_epsilon, self.epsilon * self.epsilon_decay)
        return action

    def update(self, action, reward):
        '''Update action values based on reward.'''
        a = int(action)
        self.action_counts[a] += 1
        if self.alpha is None:
            # Sample-average update
            step_size = 1.0 / self.action_counts[a]
        else:
            step_size = self.alpha
        self.q_values[a] += step_size * (float(reward) - self.q_values[a])

    def _infer_n_actions(self, action_space):
        if hasattr(action_space, "n"):
            return int(action_space.n)
        if hasattr(action_space, "__len__"):
            return len(action_space)
        if isinstance(action_space, int):
            return int(action_space)
        raise ValueError("Unable to infer number of actions from action_space")

    def _random_action(self):
        if hasattr(self.action_space, "sample"):
            return self.action_space.sample()
        return int(self.rng.integers(self.n_actions))
