
import random
from typing import Tuple, Dict, List, Any, Iterable
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
        >>> labels = {"cls": [0, 1, 2], "texts": [["cat"], ["dog"], ["bird"]], "all_texts": {0:["cat"],1:["dog"],2:["bird"],3:["elephant"],4:["car"]}}
        >>> updated_labels = loader(labels)
        >>> print(updated_labels["texts"])
        ['Object: cat', 'Object: dog', 'Object: bird', 'Object: elephant', 'Object: car']
    '''

    def __init__(self,
                 prompt_format: str = '{}',
                 neg_samples: Tuple[int, int] = (80, 80),
                 max_samples: int = 80,
                 padding: bool = False,
                 padding_value: str = '') -> None:
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
        '''
        # Extract current class indices
        cls = labels.get('cls')
        if cls is None:
            raise ValueError("labels must contain 'cls' key")
        # Convert to 1D numpy array
        cls_arr = np.array(cls).flatten()
        # Extract positive texts
        texts = labels.get('texts')
        if texts is None:
            raise ValueError("labels must contain 'texts' key")
        # Flatten texts to list of strings
        pos_texts = []
        for t in texts:
            if isinstance(t, Iterable) and not isinstance(t, (str, bytes)):
                pos_texts.extend(t)
            else:
                pos_texts.append(t)
        # Format positive texts
        formatted_pos_texts = [self.prompt_format.format(t) for t in pos_texts]
        # Determine number of negative samples
        neg_min, neg_max = self.neg_samples
        # Ensure we don't exceed max_samples
        max_neg = max(0, self.max_samples - len(formatted_pos_texts))
        if neg_min > max_neg:
            neg_min = max_neg
        if neg_max > max_neg:
            neg_max = max_neg
        if neg_min > neg_max:
            neg_min = neg_max
        num_neg = random.randint(neg_min, neg_max) if neg_min <= neg_max else 0
        # Prepare negative texts
        formatted_neg_texts: List[str] = []
        all_texts = labels.get('all_texts')
        if all_texts is not None and isinstance(all_texts, dict):
            # Get all class indices
            all_cls = set(all_texts.keys())
            # Determine negative class indices
            neg_cls_candidates = list(all_cls - set(cls_arr))
            if neg_cls_candidates:
                # Sample negative class indices
                if len(neg_cls_candidates) >= num_neg:
                    neg_cls_samples = random.sample(
                        neg_cls_candidates, num_neg)
                else:
                    neg_cls_samples = random.choices(
                        neg_cls_candidates, k=num_neg)
                # For each negative class, pick a random text
                for neg_cls in neg_cls_samples:
                    texts_for_cls = all_texts.get(neg_cls, [])
                    if
