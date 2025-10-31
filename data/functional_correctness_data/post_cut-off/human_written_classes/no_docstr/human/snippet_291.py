class State:
    UNINITIALIZED = 0
    WEIGHT_SYNCED = 1
    PROMPT_FETCH_END = 1 << 1
    PROMPT_CONSUME_END = 1 << 2
    _state: int = UNINITIALIZED

    def __init__(self):
        self._state = self.UNINITIALIZED

    def weight_synced(self):
        return self._state & self.WEIGHT_SYNCED != 0

    def set_weight_synced(self):
        self._state = self._state | self.WEIGHT_SYNCED

    def prompt_fetch_end(self):
        return self._state & self.PROMPT_FETCH_END != 0

    def set_prompt_fetch_end(self):
        self._state = self._state | self.PROMPT_FETCH_END

    def prompt_consume_end(self):
        return self._state & self.PROMPT_CONSUME_END != 0

    def set_prompt_consume_end(self):
        assert not self.prompt_consume_end(), 'Prompt consume end event should not be set twice.'
        self._state = self._state | self.PROMPT_CONSUME_END