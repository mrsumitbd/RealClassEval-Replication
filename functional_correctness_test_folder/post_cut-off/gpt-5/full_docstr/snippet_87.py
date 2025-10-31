from typing import Tuple, List, Dict, Any
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
        if not isinstance(prompt_format, str):
            raise TypeError("prompt_format must be a string")
        if '{}' not in prompt_format:
            # Allow prompts without placeholder; we'll append text at the end
            # but keep the format API by adding {} if missing.
            prompt_format = prompt_format + ' {}'
        if (not isinstance(neg_samples, tuple) or len(neg_samples) != 2 or
                not all(isinstance(x, int) for x in neg_samples)):
            raise TypeError("neg_samples must be a tuple of two integers")
        nmin, nmax = neg_samples
        if nmin < 0 or nmax < 0 or nmin > nmax:
            raise ValueError("neg_samples must be non-negative and min <= max")
        if not isinstance(max_samples, int) or max_samples <= 0:
            raise ValueError("max_samples must be a positive integer")
        if not isinstance(padding, bool):
            raise TypeError("padding must be a boolean")
        if not isinstance(padding_value, str):
            raise TypeError("padding_value must be a string")

        self.prompt_format = prompt_format
        self.neg_samples = (nmin, nmax)
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
            >>> labels = {"cls": np.array([[0], [1], [2]]), "texts": [["dog"], ["cat"], ["bird"]]}
            >>> updated_labels = loader(labels)
        '''
        if 'texts' not in labels or 'cls' not in labels:
            raise KeyError("labels must contain 'texts' and 'cls' keys")

        all_class_texts = labels['texts']
        if not isinstance(all_class_texts, (list, tuple)):
            raise TypeError("'texts' must be a list or tuple")
        # Normalize class texts to list of list[str]
        norm_texts: List[List[str]] = []
        for t in all_class_texts:
            if isinstance(t, (list, tuple)):
                norm_texts.append([str(x) for x in t] if len(t) > 0 else [])
            elif isinstance(t, str):
                norm_texts.append([t])
            else:
                norm_texts.append([str(t)])
        num_total_classes = len(norm_texts)

        # Normalize cls to 1D numpy array of ints
        cls_arr = labels['cls']
        if isinstance(cls_arr, np.ndarray):
            flat_cls = np.asarray(cls_arr).reshape(-1)
        elif isinstance(cls_arr, (list, tuple)):
            flat_cls = np.asarray(list(cls_arr)).reshape(-1)
        else:
            flat_cls = np.asarray([cls_arr]).reshape(-1)
        if flat_cls.size == 0:
            present_classes: List[int] = []
        else:
            flat_cls = flat_cls.astype(int, copy=False)
            present_classes = [int(c) for c in np.unique(flat_cls)]
        # Filter invalid classes
        present_classes = [
            c for c in present_classes if 0 <= c < num_total_classes]

        # Sample one positive text per present class
        sampled_texts: List[str] = []
        class_to_index: Dict[int, int] = {}
        for c in present_classes:
            candidates = norm_texts[c]
            if len(candidates) == 0:
                base_text = str(c)
            else:
                base_text = random.choice(candidates)
            formatted = self.prompt_format.format(base_text)
            class_to_index[c] = len(sampled_texts)
            sampled_texts.append(formatted)
            if len(sampled_texts) >= self.max_samples:
                break  # No capacity for negatives or more positives

        # Compute negative candidates and sample negatives
        remaining_capacity = max(self.max_samples - len(sampled_texts), 0)
        neg_candidates = [c for c in range(
            num_total_classes) if c not in class_to_index]
        if remaining_capacity > 0 and len(neg_candidates) > 0:
            nmin, nmax = self.neg_samples
            # Cap desired negatives to feasible range
            desired = random.randint(nmin, nmax)
            feasible_max = min(remaining_capacity, len(neg_candidates))
            desired = max(0, min(desired, feasible_max))
            if desired > 0:
                sampled_neg_classes = random.sample(neg_candidates, desired)
                for c in sampled_neg_classes:
                    candidates = norm_texts[c]
                    if len(candidates) == 0:
                        base_text = str(c)
                    else:
                        base_text = random.choice(candidates)
                    formatted = self.prompt_format.format(base_text)
                    sampled_texts.append(formatted)
                    if len(sampled_texts) >= self.max_samples:
                        break

        # Padding if required
        if self.padding and len(sampled_texts) < self.max_samples:
            pad_needed = self.max_samples - len(sampled_texts)
            pad_text = self.padding_value
            # If padding_value is empty, still format to keep style consistent
            try:
                pad_formatted = self.prompt_format.format(pad_text)
            except Exception:
                pad_formatted = pad_text
            sampled_texts.extend([pad_formatted] * pad_needed)

        # Update cls to indices in sampled_texts (for present classes only)
        # For any class without a positive entry due to capacity limits, map to -1
        new_cls_flat = []
        for c in flat_cls:
            new_idx = class_to_index.get(int(c), -1)
            new_cls_flat.append(new_idx)
        new_cls_flat = np.asarray(new_cls_flat, dtype=int)
        # Reshape to original shape where possible
        if isinstance(cls_arr, np.ndarray):
            new_cls = new_cls_flat.reshape(cls_arr.shape)
        else:
            new_cls = new_cls_flat.tolist()

        out = dict(labels)
        out['texts'] = sampled_texts
        out['cls'] = new_cls
        return out
