class SimpleAgent:

    def __init__(self, action_space, epsilon=0.1):
        self.epsilon = float(epsilon)
        self._init_actions(action_space)
        self.counts = {a: 0 for a in self.actions}
        self.values = {a: 0.0 for a in self.actions}

    def _init_actions(self, action_space):
        if hasattr(action_space, "n"):
            self.actions = list(range(int(action_space.n)))
        elif isinstance(action_space, int):
            self.actions = list(range(action_space))
        else:
            try:
                self.actions = list(action_space)
            except TypeError:
                raise ValueError(
                    "Unsupported action_space type. Provide discrete count, iterable, or object with attribute 'n'.")

        if len(self.actions) == 0:
            raise ValueError("Action space must contain at least one action.")

    def select_action(self, observation):
        import random
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        # Exploit: choose action with max estimated value; tie-break randomly
        max_value = max(self.values[a] for a in self.actions)
        best_actions = [a for a in self.actions if self.values[a] == max_value]
        return random.choice(best_actions)

    def update(self, action, reward):
        if action not in self.counts:
            # Allow unseen actions to be added dynamically
            self.actions.append(action)
            self.counts[action] = 0
            self.values[action] = 0.0
        self.counts[action] += 1
        n = self.counts[action]
        value = self.values[action]
        self.values[action] = value + (reward - value) / n
