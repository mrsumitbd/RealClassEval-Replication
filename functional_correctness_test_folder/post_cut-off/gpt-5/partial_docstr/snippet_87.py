from typing import Tuple, List, Dict, Any
import random


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

    def __init__(self, prompt_format: str = '{}', neg_samples: Tuple[int, int] = (80, 80), max_samples: int = 80,
                 padding: bool = False, padding_value: str = ''):
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
            raise TypeError("prompt_format must be a string.")
        if '{}' not in prompt_format:
            # Allow plain string but still apply by concatenation
            # To enforce strictness, we could raise, but we fallback to append behavior.
            pass
        if (not isinstance(neg_samples, tuple) or len(neg_samples) != 2 or
                not all(isinstance(x, int) for x in neg_samples)):
            raise TypeError(
                "neg_samples must be a tuple of two integers (min, max).")
        if neg_samples[0] > neg_samples[1]:
            raise ValueError("neg_samples min cannot be greater than max.")
        if not isinstance(max_samples, int) or max_samples <= 0:
            raise ValueError("max_samples must be a positive integer.")
        if not isinstance(padding, bool):
            raise TypeError("padding must be a boolean.")
        if not isinstance(padding_value, str):
            raise TypeError("padding_value must be a string.")

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
        if not isinstance(labels, dict):
            raise TypeError("labels must be a dict.")
        if "texts" not in labels or "cls" not in labels:
            raise KeyError("labels must include 'texts' and 'cls' keys.")

        all_class_texts = labels["texts"]

        # Normalize all_class_texts to list[list[str]]
        if not isinstance(all_class_texts, list):
            raise TypeError("'texts' must be a list per class.")
        normalized_texts: List[List[str]] = []
        for entry in all_class_texts:
            if isinstance(entry, list):
                # ensure list of strings
                normalized_texts.append([str(t)
                                        for t in entry] if entry else [""])
            else:
                normalized_texts.append([str(entry)])

        num_classes = len(normalized_texts)

        # Normalize cls to flat list of ints
        cls_raw = labels["cls"]
        pos_cls_list: List[int]
        try:
            import numpy as np  # optional
            if isinstance(cls_raw, (list, tuple)):
                # Flatten nested lists
                flat = []
                for c in cls_raw:
                    if isinstance(c, (list, tuple)) and len(c) == 1:
                        flat.append(int(c[0]))
                    else:
                        flat.append(int(c))
                pos_cls_list = [int(x) for x in flat]
            else:
                arr = np.asarray(cls_raw).reshape(-1)
                pos_cls_list = [int(x) for x in arr.tolist()]
        except Exception:
            # Fallback without numpy
            if isinstance(cls_raw, (list, tuple)):
                flat = []
                for c in cls_raw:
                    if isinstance(c, (list, tuple)) and len(c) == 1:
                        flat.append(int(c[0]))
                    else:
                        flat.append(int(c))
                pos_cls_list = [int(x) for x in flat]
            else:
                pos_cls_list = [int(cls_raw)]

        # Keep only valid class ids and preserve order of first occurrence
        seen = set()
        pos_cls_ordered: List[int] = []
        for cid in pos_cls_list:
            if 0 <= cid < num_classes and cid not in seen:
                seen.add(cid)
                pos_cls_ordered.append(cid)

        # Always include all positives, even if exceeding max_samples
        # Select a representative text for each positive class
        sampled_texts: List[str] = []
        class_to_index: Dict[int, int] = {}

        for cid in pos_cls_ordered:
            choices = normalized_texts[cid]
            chosen = random.choice(choices) if choices else ""
            formatted = self.prompt_format.format(
                chosen) if '{}' in self.prompt_format else f"{self.prompt_format}{chosen}"
            class_to_index[cid] = len(sampled_texts)
            sampled_texts.append(formatted)

        # Determine negatives to sample
        remaining_classes = [i for i in range(num_classes) if i not in seen]
        if len(sampled_texts) < self.max_samples and remaining_classes:
            neg_min, neg_max = self.neg_samples
            k = random.randint(neg_min, neg_max)
            # Limit by availability and max_samples budget
            budget = self.max_samples - len(sampled_texts)
            k = max(0, min(k, len(remaining_classes), budget))
            if k > 0:
                neg_classes = random.sample(remaining_classes, k)
                for cid in neg_classes:
                    choices = normalized_texts[cid]
                    chosen = random.choice(choices) if choices else ""
                    formatted = self.prompt_format.format(
                        chosen) if '{}' in self.prompt_format else f"{self.prompt_format}{chosen}"
                    sampled_texts.append(formatted)
                # Note: negatives do not get added to class_to_index, only positives map to indices

        # Optional padding
        if self.padding and len(sampled_texts) < self.max_samples:
            pad_needed = self.max_samples - len(sampled_texts)
            sampled_texts.extend([self.padding_value] * pad_needed)

        # Update cls to indices within sampled_texts: map each instance's class to its positive index
        # Instances belonging to classes not in pos_cls_ordered (invalid) will be filtered out
        new_cls_indices: List[int] = []
        for cid in pos_cls_list:
            if cid in class_to_index:
                new_cls_indices.append(class_to_index[cid])
            # else skip invalid class ids silently

        # Preserve original shape if possible
        # If original was a nested column vector, return as list of [idx]
        # Otherwise, return as flat list
        # Heuristic: if any entry in original cls was a sequence, return column format
        original_column_like = False
        if isinstance(labels["cls"], (list, tuple)):
            for c in labels["cls"]:
                if isinstance(c, (list, tuple)):
                    original_column_like = True
                    break
        try:
            import numpy as np
            if hasattr(labels["cls"], "shape"):
                # Consider (N,1) as column-like
                arr = np.asarray(labels["cls"])
                if len(arr.shape) == 2 and arr.shape[1] == 1:
                    original_column_like = True
        except Exception:
            pass

        if original_column_like:
            updated_cls = [[idx] for idx in new_cls_indices]
        else:
            updated_cls = new_cls_indices

        updated = dict(labels)
        updated["texts"] = sampled_texts
        updated["cls"] = updated_cls
        return updated
