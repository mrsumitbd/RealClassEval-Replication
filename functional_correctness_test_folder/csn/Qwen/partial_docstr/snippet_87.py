
class ContextFlag:
    '''A context manager which is also used as a boolean flag value within the default sigint handler.
    Its main use is as a flag to prevent the SIGINT handler in cmd2 from raising a KeyboardInterrupt
    while a critical code section has set the flag to True. Because signal handling is always done on the
    main thread, this class is not thread-safe since there is no need.
        '''

    def __init__(self) -> None:
        self._flag = False

    def __bool__(self) -> bool:
        return self._flag

    def __enter__(self) -> None:
        '''When a with block is entered, the __enter__ method of the context manager is called.'''
        self._flag = True

    def __exit__(self, *args: object) -> None:
        '''When the execution flow exits a with statement block this is called, regardless of whether an exception occurred.'''
        self._flag = False
