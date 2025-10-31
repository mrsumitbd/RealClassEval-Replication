
import random
from typing import Tuple, List, Dict, Any
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
        >>> labels = {"cls": [0, 1, 2], "texts": [["cat"], ["dog"], ["bird"]], "all_texts": ["cat","dog","bird","elephant","car","mouse","lion"]}
        >>> updated_labels = loader(labels)
        >>> print(updated_labels["texts"])
        ['Object: cat', 'Object: dog', 'Object: bird', 'Object: elephant', 'Object: car']
    '''

    def __init__(
        self,
        prompt_format: str = "{}",
        neg_samples: Tuple[int, int] = (80, 80),
        max_samples: int = 80,
        padding: bool = False,
        padding_value: str = "",
    ):
        """
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
        """
        self.prompt_format = prompt_format
        self.neg_samples = neg_samples
        self.max_samples = max_samples
        self.padding = padding
        self.padding_value = padding_value

    def __call__(self, labels: Dict[str, Any]) -> Dict[str, Any]:
        """
        Randomly samples positive and negative texts and updates class indices accordingly.
        This method samples positive texts based on the existing class labels in the image, and randomly
        selects negative texts from the remaining classes. It then updates the class indices to match the
        new sampled text order.
        Args:
            labels (Dict): A dictionary containing image labels and metadata. Must include 'texts' and 'cls' keys.
                It should also contain 'all_texts' key which is a list of all possible class texts.
        Returns:
            (Dict): Updated labels dictionary with new 'cls' and 'texts' entries.
        """
        # Validate input
        if "texts" not in labels or "cls" not in labels:
            raise ValueError("labels must contain 'texts' and 'cls' keys")
        if "all_texts" not in labels:
            raise ValueError(
                "labels must contain 'all_texts' key for negative sampling")

        # Positive texts
        pos_texts_raw = labels["texts"]
        # Flatten list of lists if needed
        pos_texts = [t[0] if isinstance(
            t, (list, tuple)) else t for t in pos_texts_raw]
        pos_set = set(pos_texts)

        # All texts pool
        all_texts = labels["all_texts"]
        if not isinstance(all_texts, list):
            raise ValueError("'all_texts' must be a list of strings")

        # Negative pool
        neg_pool = [t for t in all_texts if t not in pos_set]
        # Determine number of negatives to sample
        min_neg, max_neg = self.neg_samples
        # Ensure we don't exceed available negatives
        max_possible_neg = len(neg_pool)
        # If max_neg > available, adjust
        max_neg = min(max_neg, max_possible_neg)
        min_neg = min(min_neg, max_neg)
        if max_neg < min_neg:
            min_neg = max_neg
        # Randomly choose number of negatives
        num_neg = random.randint(min_neg, max_neg) if max_neg > 0 else 0
        # Sample negatives
        neg_texts = random.sample(neg_pool, num_neg) if num_neg > 0 else []

        # Combine positives and negatives
        combined_texts = pos_texts + neg_texts

        # If padding is enabled, pad to max_samples
        if self.padding:
            if len(combined_texts) < self.max_samples:
                pad_count = self.max_samples - len(combined_texts)
                combined
