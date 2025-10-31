
import random
from typing import Tuple, Dict, List, Any, Optional
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
        >>> labels = {"cls": [0, 1, 2], "texts": [["cat"], ["dog"], ["bird"]], "all_texts": {3: ["elephant"], 4: ["car"]}}
        >>> updated_labels = loader(labels)
        >>> print(updated_labels["texts"])
        ['Object: cat', 'Object: dog', 'Object: bird',
            'Object: elephant', 'Object: car']
    '''

    def __init__(
        self,
        prompt_format: str = "{}",
        neg_samples: Tuple[int, int] = (80, 80),
        max_samples: int = 80,
        padding: bool = False,
        padding_value: str = "",
    ):
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
        self.prompt_format = prompt_format
        self.neg_samples = neg_samples
        self.max_samples = max_samples
        self.padding = padding
        self.padding_value = padding_value

    def __call__(self, labels: Dict[str, Any]) -> Dict[str, Any]:
        '''
        Randomly samples positive and negative texts and updates class indices accordingly.
        This method samples positive texts based on the existing class labels in the image, and randomly
        selects negative texts from the remaining classes. It then updates the class indices to match the
        new sampled text order.
        Args:
            labels (Dict): A dictionary containing image labels and metadata. Must include 'texts' and 'cls' keys.
        Returns:
            (Dict): Updated labels dictionary with new 'cls' and 'texts' entries.
        Examples:
            >>> loader = RandomLoadText(prompt_format="A photo of {}", neg_samples=(5, 10), max_samples=20)
            >>> labels = {"cls": np.array([[0], [1], [2]]), "texts": [["dog"], ["cat"], ["bird"]], "all_texts": {3: ["elephant"], 4: ["car"]}}
            >>> updated_labels = loader(labels)
        '''
        # Extract class indices
        cls = labels.get("cls")
        if cls is None:
            raise ValueError("labels must contain 'cls' key")
        # Flatten cls to 1D list
        if isinstance(cls, np.ndarray):
            cls_list = cls.flatten().tolist()
        else:
            cls_list = list(cls)

        # Extract texts per instance
        texts_per_instance = labels.get("texts")
        if texts_per_instance is None:
            raise ValueError("labels must contain 'texts' key")
        # Flatten to list of strings (take first element if list)
        positive_texts = []
        for t in texts_per_instance:
            if isinstance(t, (list, tuple)):
                if len(t) > 0:
                    positive_texts.append(str(t[0]))
                else:
                    positive_texts.append("")
            else:
                positive_texts.append(str(t))

        # Unique positive texts
        unique_positive_texts = list(dict.fromkeys(positive_texts))

        # Build negative pool from all_texts if provided
        all_texts = labels.get("all_texts", {})
        negative_pool: List[str] = []
        positive_set = set(cls_list)
        for cls_idx, txt_list in all_texts.items():
            if cls_idx not in positive_set:
                negative_pool.extend([str(t) for
