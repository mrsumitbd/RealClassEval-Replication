import random
from typing import Tuple, List, Dict, Any


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
        >>> labels = {"cls": [0, 1, 2], "texts": [["cat"], ["dog"], ["bird"]], "instances": [...]}
        >>> updated_labels = loader(labels)
        >>> print(updated_labels["texts"])
        ['Object: cat', 'Object: dog', 'Object: bird', 'Object: elephant', 'Object: car']
    '''

    def __init__(
        self,
        prompt_format: str = '{}',
        neg_samples: Tuple[int, int] = (80, 80),
        max_samples: int = 80,
        padding: bool = False,
        padding_value: str = ''
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
        Attributes:
            prompt_format (str): The format string for the prompt.
            neg_samples (Tuple[int, int]): The range for sampling negative texts.
            max_samples (int): The maximum number of text samples.
            padding (bool): Whether padding is enabled.
            padding_value (str): The value used for padding.
        Examples:
            >>> random_load_text = RandomLoadText(prompt_format="Object: {}", neg_samples=(50, 100), max_samples=120)
            >>> random_load_text.prompt_format
            'Object: {}'
            >>> random_load_text.neg_samples
            (50, 100)
            >>> random_load_text.max_samples
            120
        '''
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
            labels (Dict): A dictionary containing image labels and metadata. Must include 'texts' and 'cls' keys.
        Returns:
            (Dict): Updated labels dictionary with new 'cls' and 'texts' entries.
        Examples:
            >>> loader = RandomLoadText(prompt_format="A photo of {}", neg_samples=(5, 10), max_samples=20)
            >>> labels = {"cls": np.array([[0], [1], [2]]), "texts": [["dog"], ["cat"], ["bird"]]}
            >>> updated_labels = loader(labels)
        '''
        # Extract all class texts and positive class indices
        all_texts = labels.get('all_texts', None)
        if all_texts is None:
            # If not provided, infer from 'texts'
            # Assume 'texts' is a list of lists, each sublist is the text(s) for a class
            all_texts = [t[0] if isinstance(
                t, (list, tuple)) else t for t in labels['texts']]
        else:
            # If provided, flatten if needed
            if isinstance(all_texts[0], (list, tuple)):
                all_texts = [t[0] if isinstance(
                    t, (list, tuple)) else t for t in all_texts]

        # Get positive class indices and texts
        cls = labels['cls']
        if hasattr(cls, 'tolist'):
            cls = cls.tolist()
        if isinstance(cls, list) and isinstance(cls[0], (list, tuple)):
            cls = [c[0] for c in cls]
        pos_indices = list(set(cls))
        pos_indices = [int(i) for i in pos_indices]
        pos_indices = [i for i in pos_indices if i < len(all_texts)]
        pos_texts = [all_texts[i] for i in pos_indices]

        # Negative indices: all except positive
        all_indices = list(range(len(all_texts)))
        neg_indices = [i for i in all_indices if i not in pos_indices]

        # How many negative samples?
        min_neg, max_neg = self.neg_samples
        if min_neg == max_neg:
            num_neg = min_neg
        else:
            num_neg = random.randint(min_neg, max_neg)
        # Limit so that total samples do not exceed max_samples
        num_pos = len(pos_indices)
        num_neg = min(num_neg, max(
            0, self.max_samples - num_pos, len(neg_indices)))
        # Sample negative indices
        neg_indices_sampled = random.sample(
            neg_indices, num_neg) if num_neg > 0 and len(neg_indices) > 0 else []
        neg_texts = [all_texts[i] for i in neg_indices_sampled]

        # Compose the new text list: positive first, then negative
        sampled_texts = pos_texts + neg_texts
        # Map: new index in sampled_texts -> original class index
        sampled_indices = pos_indices + neg_indices_sampled

        # If padding is enabled, pad to max_samples
        if self.padding and len(sampled_texts) < self.max_samples:
            pad_count = self.max_samples - len(sampled_texts)
            sampled_texts += [self.padding_value] * pad_count
            sampled_indices += [-1] * pad_count  # -1 for padding

        # Format texts
        formatted_texts = [self.prompt_format.format(
            t) if t != self.padding_value else self.padding_value for t in sampled_texts]

        # Update class indices in labels to match new text order
        # For each original class in labels['cls'], find its new index in sampled_indices
        old_cls = labels['cls']
        if hasattr(old_cls, 'tolist'):
            old_cls = old_cls.tolist()
        if isinstance(old_cls, list) and isinstance(old_cls[0], (list, tuple)):
            old_cls = [c[0] for c in old_cls]
        new_cls = []
        for c in old_cls:
            if c in sampled_indices:
                new_idx = sampled_indices.index(c)
            else:
                # If not found (should not happen for positive classes), set to -1
                new_idx = -1
            new_cls.append([new_idx])
        # If original was numpy array, convert back
        try:
            import numpy as np
            if isinstance(labels['cls'], np.ndarray):
                new_cls = np.array(new_cls, dtype=labels['cls'].dtype)
        except ImportError:
            pass

        # Update labels
        labels = dict(labels)
        labels['texts'] = formatted_texts
        labels['cls'] = new_cls
        return labels
