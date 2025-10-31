class PrintOnce:
    """
    Class for printing messages just once. Can be useful when running in a loop
    """

    def __init__(self, print_callback) -> None:
        self.already_printed = False
        self.print_callback = print_callback

    def __call__(self, text) -> None:
        if not self.already_printed:
            self.print_callback(text)
            self.already_printed = True