class Brute:
    """
    Implementation of the Brute

    Creates and manages the tree storing game actions and rewards
    """

    def __init__(self, env, max_episode_steps):
        self.node_count = 1
        self._root = Node()
        self._env = env
        self._max_episode_steps = max_episode_steps

    def run(self):
        acts = select_actions(self._root, self._env.action_space, self._max_episode_steps)
        steps, total_rew = rollout(self._env, acts)
        executed_acts = acts[:steps]
        self.node_count += update_tree(self._root, executed_acts, total_rew)
        return (executed_acts, total_rew)