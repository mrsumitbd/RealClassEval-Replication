import os

class ScopedEnvVar:
    """Temporarily change an environment variable

    Usage:
        with ScopedEnvVar("FOO", "bar"):
            print(os.environ["FOO"]) # "bar"
        print(os.environ["FOO"]) # <oldvalue>
    """

    def __init__(self, name, value):
        """Create the scoped environment variable object

        name -- Name of the variable to set
        value -- Value to use or None to clear
        """
        self.name = name
        self.value = value
        self.oldValue = None

    def __enter__(self):
        self.oldValue = os.environ.get(self.name)
        setEnvVar(self.name, self.value)
        return self

    def __exit__(self, ex_type, ex_value, traceback):
        setEnvVar(self.name, self.oldValue)