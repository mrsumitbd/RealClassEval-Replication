from collections.abc import Generator, Iterable

class IterableAugmentor:

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
        self.is_generator = True

    def __call__(self, data: Iterable) -> Generator:
        """Example usage:

        for data_dict in data:
            # Do something to data_dict
            data_dict["input"] = data_dict["raw_sequence"][:, :-1]
            data_dict["target"] = data_dict["raw_sequence"][:, 1:]
            # Skip sample if needed
            if data_dict["input"].shape[1] < 64:
                continue
            # Construct a generator
            yield data_dict
        """
        raise ValueError('Augmentor not implemented')