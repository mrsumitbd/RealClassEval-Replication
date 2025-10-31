
import random


class SimpleAgent:
    def __init__(self, action_space):
        """
        Initialize the agent with a given action space.

        Parameters
        ----------
        action_space : iterable
            A collection of possible actions the agent can take.
        """
        self.action_space = list(action_space)

    def select_action(self, observation):
        """
        Select an action based on the current observation.

        Parameters
        ----------
        observation : any
            The current observation from the environment (unused in this simple agent).

        Returns
        -------
        action : any
            A randomly chosen action from the action space.
        """
        if not self.action_space:
            raise ValueError("Action space is empty.")
        return random.choice(self.action_space)

    def update(self, action, reward):
        """
        Update the agent's internal state based on the action taken and the reward received.

        Parameters
        ----------
        action : any
            The action that was taken.
        reward : float
            The reward received after taking the action.

        Notes
        -----
        This simple agent does not learn from the reward, so the method is a no-op.
        """
        pass
