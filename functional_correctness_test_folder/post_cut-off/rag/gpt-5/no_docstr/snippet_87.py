from typing import Tuple, List, Dict, Any, Sequence
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

    def __init__(self, prompt_format: str = '{}', neg_samples: Tuple[int, int] = (80, 80),
                 max_samples: int = 80, padding: bool = False, padding_value: str = '') -> None:
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
        if not isinstance(prompt_format, str):
            raise TypeError('prompt_format must be a string')
        if '{}' not in prompt_format:
            raise ValueError("prompt_format must contain '{}' placeholder")
        if isinstance(neg_samples, int):
            neg_samples = (neg_samples, neg_samples)
        if (not isinstance(neg_samples, (tuple, list))) or len(neg_samples) != 2:
            raise TypeError('neg_samples must be a tuple of two integers')
        nmin, nmax = int(neg_samples[0]), int(neg_samples[1])
        if nmin < 0 or nmax < 0 or nmin > nmax:
            raise ValueError('neg_samples must be non-negative and min <= max')
        if not isinstance(max_samples, int) or max_samples <= 0:
            raise ValueError('max_samples must be a positive integer')

        self.prompt_format: str = prompt_format
        self.neg_samples: Tuple[int, int] = (nmin, nmax)
        self.max_samples: int = max_samples
        self.padding: bool = bool(padding)
        self.padding_value: str = padding_value

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
            raise KeyError("labels must contain 'texts' and 'cls' keys")

        all_texts_raw = labels['texts']
        if not isinstance(all_texts_raw, Sequence):
            raise TypeError("'texts' must be a sequence of per-class texts")

        # Normalize texts per class to List[List[str]]
        texts_per_class: List[List[str]] = []
        for t in all_texts_raw:
            if isinstance(t, str):
                texts_per_class.append([t])
            elif isinstance(t, Sequence):
                # filter to strings only
                strings = [str(x) for x in t]
                if len(strings) == 0:
                    strings = ['']
                texts_per_class.append(strings)
            else:
                texts_per_class.append([str(t)])

        num_classes = len(texts_per_class)

        # Normalize cls to a 1D list of ints
        cls_arr = labels['cls']
        if isinstance(cls_arr, np.ndarray):
            flat_cls = cls_arr.reshape(-1).astype(int).tolist()
            input_shape = cls_arr.shape
            is_numpy = True
        else:
            flat_cls = [int(c) for c in cls_arr]
            input_shape = (len(flat_cls),)
            is_numpy = False

        # Keep only valid class indices
        flat_cls = [c for c in flat_cls if 0 <= c < num_classes]

        # Positive classes in order of first appearance
        seen = set()
        pos_classes: List[int] = []
        for c in flat_cls:
            if c not in seen:
                seen.add(c)
                pos_classes.append(c)

        # Select one positive text per positive class
        pos_texts: List[str] = []
        class_to_new_index: Dict[int, int] = {}
        for idx, c in enumerate(pos_classes):
            chosen = random.choice(texts_per_class[c])
            pos_texts.append(self.prompt_format.format(chosen))
            class_to_new_index[c] = idx

        # Negative sampling
        neg_candidates = [c for c in range(num_classes) if c not in seen]
        min_neg, max_neg = self.neg_samples
        requested_neg = random.randint(min_neg, max_neg)

        # Ensure we always include positives; extend budget if positives exceed configured max
        actual_max = max(self.max_samples, len(pos_classes))
        neg_budget = max(0, actual_max - len(pos_classes))
        nneg = min(requested_neg, neg_budget, len(neg_candidates))
        if nneg > 0:
            sampled_neg_classes = random.sample(neg_candidates, nneg)
        else:
            sampled_neg_classes = []

        neg_texts: List[str] = []
        for c in sampled_neg_classes:
            chosen = random.choice(texts_per_class[c])
            neg_texts.append(self.prompt_format.format(chosen))

        combined_texts: List[str] = pos_texts + neg_texts

        # Padding
        if self.padding:
            if len(combined_texts) < actual_max:
                combined_texts.extend(
                    [self.padding_value] * (actual_max - len(combined_texts)))

        # Remap cls to new indices (positives only)
        new_cls = [class_to_new_index[c]
                   for c in flat_cls if c in class_to_new_index]

        # Restore original shape/type for cls
        if is_numpy:
            # infer if original was column vector
            if len(input_shape) == 2 and (input_shape[1] == 1 or input_shape[0] == 1):
                new_cls_arr = np.asarray(
                    new_cls, dtype=np.int64).reshape(-1, 1)
            else:
                new_cls_arr = np.asarray(new_cls, dtype=np.int64)
            labels_out = dict(labels)
            labels_out['cls'] = new_cls_arr
        else:
            labels_out = dict(labels)
            labels_out['cls'] = new_cls

        labels_out['texts'] = combined_texts
        return labels_out
