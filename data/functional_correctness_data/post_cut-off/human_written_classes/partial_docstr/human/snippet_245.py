from typing import Any

class Augmentor:

    def __init__(self, input_keys: list, output_keys: list | None=None, args: dict | None=None) -> None:
        """Base augmentor class

        Args:
            input_keys (list): List of input keys
            output_keys (list): List of output keys
            args (dict): Arguments associated with the augmentation
        """
        self.input_keys = input_keys
        self.output_keys = output_keys
        self.args = args

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        raise ValueError('Augmentor not implemented')