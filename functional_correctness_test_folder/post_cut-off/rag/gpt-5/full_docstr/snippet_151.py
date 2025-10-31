import random


class SimpleAgent:
    '''
    A simple agent that selects actions for the TutorEnv.
    This is a placeholder for an actual Atropos policy.
    '''

    def __init__(self, action_space):
        '''Initialize with the action space of the environment.'''
        self._setup_action_space(action_space)

        # Action-value estimates and counts
        self.q_values = [0.0 for _ in range(self.num_actions)]
        self.action_counts = [0 for _ in range(self.num_actions)]

        # Epsilon-greedy parameters
        self.epsilon = 0.1
        self.min_epsilon = 0.01
        self.epsilon_decay = 0.995

        # Learning rate; if None, use sample-average update
        self.alpha = None

    def _setup_action_space(self, action_space):
        # Handle common Gym-like discrete action spaces
        if hasattr(action_space, 'n'):
            self.num_actions = int(action_space.n)
            self._action_from_index = lambda i: i
            self._index_from_action = lambda a: int(a)
            return

        # If an integer is given, treat it as number of discrete actions
        if isinstance(action_space, int):
            self.num_actions = int(action_space)
            self._action_from_index = lambda i: i
            self._index_from_action = lambda a: int(a)
            return

        # If a list/tuple of discrete actions is provided
        if isinstance(action_space, (list, tuple)):
            self._actions = list(action_space)
            self.num_actions = len(self._actions)
            # Try to build inverse mapping; fallback to list.index if unhashable
            try:
                self._inv_actions = {a: i for i, a in enumerate(self._actions)}
                self._index_from_action = lambda a: self._inv_actions[a]
            except TypeError:
                self._inv_actions = None
                self._index_from_action = lambda a: self._actions.index(a)
            self._action_from_index = lambda i: self._actions[i]
            return

        # As a fallback, try to infer 'n' attribute; else unsupported
        maybe_n = getattr(action_space, 'n', None)
        if maybe_n is not None:
            self.num_actions = int(maybe_n)
            self._action_from_index = lambda i: i
            self._index_from_action = lambda a: int(a)
            return

        raise ValueError('Unsupported action_space for SimpleAgent')

    def select_action(self, observation):
        '''
        Select an action based on the current observation.
        Uses simple epsilon-greedy strategy.
        '''
        # Epsilon-greedy selection (observation ignored in this simple agent)
        if random.random() < self.epsilon:
            idx = random.randrange(self.num_actions)
        else:
            max_q = max(self.q_values)
            best_indices = [i for i, q in enumerate(
                self.q_values) if q == max_q]
            idx = random.choice(best_indices)

        action = self._action_from_index(idx)

        # Decay epsilon after selection
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)
        return action

    def update(self, action, reward):
        '''Update action values based on reward.'''
        try:
            idx = self._index_from_action(action)
        except Exception:
            # If mapping fails, assume action is already an index
            idx = int(action)

        self.action_counts[idx] += 1
        step_size = self.alpha if self.alpha is not None else 1.0 / \
            self.action_counts[idx]
        self.q_values[idx] += step_size * (float(reward) - self.q_values[idx])
