from typing import Tuple, Dict, List, Any
import random
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
        self.prompt_format = str(prompt_format)
        if not isinstance(neg_samples, tuple) or len(neg_samples) != 2:
            raise ValueError(
                'neg_samples must be a tuple of two integers (min, max).')
        a, b = int(neg_samples[0]), int(neg_samples[1])
        self.neg_samples = (min(a, b), max(a, b))
        self.max_samples = int(max_samples)
        if self.max_samples < 0:
            raise ValueError('max_samples must be non-negative.')
        self.padding = bool(padding)
        self.padding_value = str(padding_value)

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
        if 'texts' not in labels or 'cls' not in labels:
            raise KeyError("labels must contain 'texts' and 'cls' keys.")

        class_texts = labels['texts']
        if not isinstance(class_texts, (list, tuple)):
            raise TypeError(
                "labels['texts'] must be a list (or tuple) of per-class texts.")
        n_classes = len(class_texts)

        # Normalize cls to numpy array and flatten
        cls_arr = np.array(labels['cls'])
        cls_flat = cls_arr.reshape(-1)

        # Extract positive classes present in the image
        pos_classes = []
        for v in cls_flat:
            try:
                idx = int(v)
            except Exception:
                continue
            if 0 <= idx < n_classes:
                pos_classes.append(idx)
        pos_classes = sorted(set(pos_classes))

        # Ensure we always keep all positives; negatives fill up to capacity
        effective_max = max(self.max_samples, len(pos_classes))

        # Helper to choose a representative text for a given class index
        def choose_text_for_class(cid: int) -> str:
            candidates = class_texts[cid]
            if isinstance(candidates, (list, tuple)) and len(candidates) > 0:
                choice = random.choice(list(candidates))
            elif isinstance(candidates, (list, tuple)) and len(candidates) == 0:
                choice = ''
            else:
                choice = str(candidates)
            return self._format_text(choice)

        # Positive texts
        pos_texts = [choose_text_for_class(c) for c in pos_classes]

        # Negative classes pool and count
        neg_pool = [c for c in range(n_classes) if c not in pos_classes]
        if len(neg_pool) > 1:
            random.shuffle(neg_pool)

        neg_min, neg_max = self.neg_samples
        # desired negatives in range
        desired_neg = random.randint(neg_min, neg_max) if neg_max >= 0 else 0
        # cap negatives to fit within effective_max and available pool
        capacity_left = max(0, effective_max - len(pos_classes))
        neg_k = max(0, min(desired_neg, capacity_left, len(neg_pool)))

        neg_classes = neg_pool[:neg_k]
        neg_texts = [choose_text_for_class(c) for c in neg_classes]

        # Final sampled order: positives first, then negatives
        sampled_classes = pos_classes + neg_classes
        sampled_texts = pos_texts + neg_texts

        # Optional padding
        if self.padding and len(sampled_texts) < self.max_samples:
            pad_count = self.max_samples - len(sampled_texts)
            pad_text = self._format_text(self.padding_value)
            sampled_texts += [pad_text] * pad_count

        # Remap original cls to new indices based on sampled_classes
        class_to_new = {cid: i for i, cid in enumerate(sampled_classes)}
        remapped = []
        for v in cls_flat:
            try:
                idx = int(v)
            except Exception:
                remapped.append(-1)
                continue
            remapped.append(class_to_new.get(idx, -1))
        remapped = np.array(remapped, dtype=np.int64).reshape(cls_arr.shape)

        # Update labels
        updated = dict(labels)
        updated['texts'] = sampled_texts
        updated['cls'] = remapped
        updated['sampled_classes'] = sampled_classes
        return updated

    def _format_text(self, text: str) -> str:
        try:
            return self.prompt_format.format(text)
        except Exception:
            return f'{self.prompt_format}{text}'
