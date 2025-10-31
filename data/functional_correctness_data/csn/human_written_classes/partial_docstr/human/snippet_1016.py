class PrintFunctionStreamWriter:
    """
    'Stream' that allows to write to a print_function.

    Parameters
    ----------
    print_function: typing.Callable
    """

    def __init__(self, print_function):
        self._print_function = print_function

    def write(self, message):
        """
        Write to stream.

        Parameters
        ----------
        message: str
        """
        message = message.strip()
        if message != '':
            self._print_function(message)