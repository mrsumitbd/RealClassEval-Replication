class BufferCnt:
    """
    Buffer counter which keeps track of the condition when called and returns True when the condition in met "thres"
    amount of times, otherwise returns False.

    Example usage:
        buf = BufferCnt(thres=3)
        for _ in range(5):
            if buf(random.random() > 0.5):
                print("We got lucky 3 times out of 5.")

    Args:
        thres (int): The amount of times the expression needs to be True before returning True.
        reset_over_thres (bool): Whether to reset the buffer after returning True.
    """

    def __init__(self, thres=10, reset_over_thres=False):
        self._cnt = 0
        self.thres = thres
        self.reset_over_thres = reset_over_thres

    def __call__(self, expre, thres=None):
        if expre is True:
            self._cnt += 1
        else:
            self._cnt = 0
        if thres is None:
            thres = self.thres
        if self._cnt >= thres:
            if self.reset_over_thres:
                self.reset()
            return True
        return False

    @property
    def cnt(self):
        return self._cnt

    def reset(self):
        self._cnt = 0