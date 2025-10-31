import argparse

class StoreOpt:
    """
    Helper class for storing lists of the options themselves to hand out to the
    shell completion scripts.
    """

    def __init__(self) -> None:
        self.options: list[str] = []
        self.actions: list[argparse.Action] = []

    def __call__(self, action: argparse.Action) -> None:
        self.actions.append(action)
        self.options.extend(action.option_strings[0:2])