class Frame:
    """
    Class that replicates just enough of the builtin Frame object to enable serialization and traceback rendering.

    Args:

        get_locals (callable): A function that take a frame argument and returns a dict.

            See :class:`Traceback` class for example.
    """

    def __init__(self, frame, *, get_locals=None):
        self.f_locals = {} if get_locals is None else get_locals(frame)
        self.f_globals = {k: v for k, v in frame.f_globals.items() if k in ('__file__', '__name__')}
        self.f_code = Code(frame.f_code)
        self.f_lineno = frame.f_lineno

    def clear(self):
        """
        For compatibility with PyPy 3.5;
        clear() was added to frame in Python 3.4
        and is called by traceback.clear_frames(), which
        in turn is called by unittest.TestCase.assertRaises
        """