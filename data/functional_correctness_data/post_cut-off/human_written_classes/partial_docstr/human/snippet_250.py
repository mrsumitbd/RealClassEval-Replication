import termcolor

class Color:
    """A convenience class to colorize strings in the console.

    Example:
        import
        print("This is {Color.red('important')}.")
    """

    @staticmethod
    def red(x: str) -> str:
        return termcolor.colored(str(x), color='red')

    @staticmethod
    def green(x: str) -> str:
        return termcolor.colored(str(x), color='green')

    @staticmethod
    def blue(x: str) -> str:
        return termcolor.colored(str(x), color='blue')

    @staticmethod
    def cyan(x: str) -> str:
        return termcolor.colored(str(x), color='cyan')

    @staticmethod
    def yellow(x: str) -> str:
        return termcolor.colored(str(x), color='yellow')

    @staticmethod
    def magenta(x: str) -> str:
        return termcolor.colored(str(x), color='magenta')

    @staticmethod
    def grey(x: str) -> str:
        return termcolor.colored(str(x), color='grey')