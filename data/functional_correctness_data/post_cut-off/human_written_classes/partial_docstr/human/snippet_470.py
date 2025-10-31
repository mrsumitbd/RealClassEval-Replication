import threading
from typing import Callable, Generator, List

class Switch:

    def __init__(self, status, get_state, name=None):
        """
        Args:
            status
                (dict):A dict describes each state.
                    {
                        0: {
                            'func': (Callable)
                        },
                        1: {
                            'func'
                            'args': (Optional, tuple)
                            'kwargs': (Optional, dict)
                        },
                        2: [
                            func1,
                            {
                                'func': func2
                                'args': args2
                            }
                        ]
                        -1: []
                    }
                (Callable):current state will pass into this function
                    lambda state: do_update(state=state)
            get_state:
                (Callable):
                    return current state
                (Generator):
                    yield current state, do nothing when state not in status
            name:
        """
        self._lock = threading.Lock()
        self.name = name
        self.status = status
        self.get_state = get_state
        if isinstance(get_state, Generator):
            self._generator = get_state
        elif isinstance(get_state, Callable):
            self._generator = self._get_state()

    @staticmethod
    def get_state():
        pass

    def _get_state(self):
        """
        Predefined generator when `get_state` is an callable
        Customize it if you have multiple criteria on state
        """
        _status = self.get_state()
        yield _status
        while True:
            status = self.get_state()
            if _status != status:
                _status = status
                yield _status
                continue
            yield (-1)

    def switch(self):
        with self._lock:
            r = next(self._generator)
        if callable(self.status):
            self.status(r)
        elif r in self.status:
            f = self.status[r]
            if isinstance(f, (dict, Callable)):
                f = [f]
            for d in f:
                if isinstance(d, Callable):
                    d = {'func': d}
                func = d['func']
                args = d.get('args', tuple())
                kwargs = d.get('kwargs', dict())
                func(*args, **kwargs)

    def g(self) -> Generator:
        g = get_generator(self.switch)
        if self.name:
            name = self.name
        else:
            name = self.get_state.__name__
        g.__name__ = f'Switch_{name}_refresh'
        return g