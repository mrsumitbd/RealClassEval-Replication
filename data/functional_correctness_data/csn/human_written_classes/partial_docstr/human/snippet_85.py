class FirstStepAccumulator:
    """Store and retrieve the train step data.

    This class simply stores the first step value and returns it.

    For most uses, ``skorch.utils.FirstStepAccumulator`` is what you
    want, since the optimizer calls the train step exactly
    once. However, some optimizerss such as LBFGSs make more than one
    call. If in that case, you don't want the first value to be
    returned (but instead, say, the last value), implement your own
    accumulator and make sure it is returned by
    ``NeuralNet.get_train_step_accumulator`` method.

    """

    def __init__(self):
        self.step = None

    def store_step(self, step):
        """Store the first step."""
        if self.step is None:
            self.step = step

    def get_step(self):
        """Return the stored step."""
        return self.step