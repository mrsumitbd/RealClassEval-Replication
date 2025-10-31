
import random
from collections import deque


class Reservoir:
    """
    A simple reservoir sampler that keeps at most `traces_per_sec` items.
    New items are added via the `add` method, and items can be retrieved
    randomly using the `take` method.
    """

    def __init__(self, traces_per_sec=0):
        """
        Initialize the reservoir.

        Parameters
        ----------
        traces_per_sec : int, optional
            The maximum number of traces to keep in the reservoir.
            Defaults to 0 (no capacity).
        """
        self.capacity = max(0, int(traces_per_sec))
        self._reservoir = deque()
        self._total_seen = 0

    def add(self, trace):
        """
        Add a new trace to the reservoir using reservoir sampling.

        Parameters
        ----------
        trace : any
            The trace to add.
        """
        self._total_seen += 1
        if len(self._reservoir) < self.capacity:
            self._reservoir.append(trace)
        else:
            # Replace an existing item with probability capacity / total_seen
            if self.capacity == 0:
                return
            if random.randint(1, self._total_seen) <= self.capacity:
                idx = random.randint(0, self.capacity - 1)
                self._reservoir[idx] = trace

    def take(self):
        """
        Retrieve and remove a random trace from the reservoir.

        Returns
        -------
        any or None
            A randomly selected trace, or None if the reservoir is empty.
        """
        if not self._reservoir:
            return None
        idx = random.randint(0, len(self._reservoir) - 1)
        # Pop the element at idx
        # Since deque doesn't support direct indexing, convert to list temporarily
        temp_list = list(self._reservoir)
        trace = temp_list.pop(idx)
        self._reservoir = deque(temp_list)
        return trace

    def __len__(self):
        """Return the current number of traces stored."""
        return len(self._reservoir)

    def __iter__(self):
        """Iterate over the traces in the reservoir."""
        return iter(self._reservoir)
