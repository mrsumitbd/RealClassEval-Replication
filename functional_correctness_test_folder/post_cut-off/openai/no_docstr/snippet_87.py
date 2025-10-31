
import random
from typing import Tuple
import numpy as np


class RandomLoadText:
    '''
    Randomly samples positive and negative texts and updates class indices accordingly.
    This class is responsible for sampling texts from a given set of class texts, including both positive
    (present in the image) and negative (not present in the image) samples. It updates the class indices
    to reflect the sampled texts and can optionally pad the text list to a fixed length.
    Attributes:
        prompt_format (str): Format string for text prompts.
        neg_samples (Tuple[int, int]): Range for randomly sampling negative texts.
        max_samples (int): Maximum number of different text samples in one image.
        padding (bool): Whether to pad texts to max_samples.
        padding_value (str): The text used for padding when padding is True.
    Methods:
        __call__: Processes the input labels and returns updated classes and texts.
    Examples:
        >>> loader = RandomLoadText(prompt_format="Object: {}", neg_samples=(5, 10), max_samples=20)
        >>> labels = {"cls": [0, 1, 2], "texts": [["cat"], ["dog"], ["bird"]], "all_texts": ["cat","dog","bird","elephant","car","mouse"] }
        >>> updated_labels = loader(labels)
        >>> print(updated_labels["texts"])
        ['Object: cat', 'Object: dog', 'Object: bird',
            'Object: elephant', 'Object: car']
    '''

    def __init__(self,
                 prompt_format: str = '{}',
                 neg_samples: Tuple[int, int] = (80, 80),
                 max_samples: int = 80,
                 padding: bool = False,
                 padding_value: str = ''):
        '''
        Initializes the RandomLoadText class for randomly sampling positive and negative texts.
        This class is designed to randomly sample positive texts and negative texts, and update the class
        indices accordingly to the number of samples. It can be used for text-based object detection tasks.
        Args:
            prompt_format (str): Format string for the prompt. Default is '{}'. The format string should
                contain a single pair of curly braces {} where the text will be inserted.
            neg_samples (Tuple[int, int]): A range to randomly sample negative texts. The first integer
                specifies the minimum number of negative samples, and the second integer specifies the
                maximum. Default is (80, 80).
            max_samples (int): The maximum number of different text samples in one image. Default is 80.
            padding (bool): Whether to pad texts to max_samples. If True, the number of texts will always
                be equal to max_samples. Default is False.
            padding_value (str): The padding text to use when padding is True. Default is an empty string.
        '''
        if not isinstance(prompt_format, str) or '{}' not in prompt_format:
            raise ValueError(
                "prompt_format must be a string containing '{}' placeholder.")
        if not (isinstance(neg_samples, tuple) and len(neg_samples) == 2 and
                all(isinstance(x, int) and x >= 0 for x in neg_samples)):
            raise ValueError(
                "neg_samples must be a tuple of two non-negative integers.")
        if neg_samples[0] > neg_samples[1]:
            raise ValueError(
                "neg_samples[0] cannot be greater than neg_samples[1].")
        if not isinstance(max_samples, int) or max_samples <= 0:
            raise ValueError("max_samples must be a positive integer.")
        if not isinstance(padding, bool):
            raise ValueError("padding must be a boolean.")
        if not isinstance(padding_value, str):
            raise ValueError("padding_value must be a string.")

        self.prompt_format = prompt_format
        self.neg_samples = neg_samples
        self.max_samples = max_samples
        self.padding = padding
        self.padding_value = padding_value

    def __call__(self, labels: dict) -> dict:
        '''
        Randomly samples positive and negative texts and updates class indices accordingly.
        This method samples positive texts based on the existing class labels in the image, and randomly
        selects negative texts from the remaining classes. It then updates the class indices to match the
        new sampled text order.
        Args:
            labels (Dict): A dictionary containing image labels and metadata. Must include 'texts' and 'cls' keys,
                           and optionally 'all_texts' key which is a list of all possible texts.
        Returns:
            (Dict): Updated labels dictionary with new 'cls' and 'texts' entries.
        Examples:
            >>> loader = RandomLoadText(prompt_format="A photo of {}", neg_samples=(5, 10), max_samples=20)
            >>> labels = {"cls": np.array([[0], [1], [2]]), "texts": [["dog"], ["cat"], ["bird"]], "all_texts": ["dog","cat","bird","elephant","car"] }
            >>> updated_labels = loader(labels)
        '''
        if 'texts' not in labels or 'cls' not in labels:
            raise KeyError("labels must contain 'texts' and 'cls' keys.")
        if 'all_texts' not in labels:
            raise KeyError(
                "labels must contain 'all_texts' key for negative sampling.")

        # Extract positive texts
        pos_texts_raw = labels['texts']
        if not isinstance(pos_texts_raw, list):
            raise ValueError("'texts' must be a list.")
        pos_texts = []
        for item in pos_texts_raw:
            if isinstance(item, list) and len(item) > 0:
                pos_texts.append(item[0])
            elif isinstance(item, str):
                pos_texts.append(item)
            else:
                raise ValueError(
                    "Each element in 'texts' must be a string or a non-empty list of strings.")

        # All possible texts
        all_texts = labels['all_texts']
        if not isinstance(all_texts
