from typing import Tuple, List, Dict, Any, Union, Sequence
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
        padding_value: str = '',
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
        if not isinstance(prompt_format, str) or '{}' not in prompt_format:
            raise ValueError(
                "prompt_format must be a string containing '{}' for insertion.")
        if (not isinstance(neg_samples, (tuple, list)) or len(neg_samples) != 2 or
                any(not isinstance(x, int) for x in neg_samples)):
            raise ValueError(
                "neg_samples must be a tuple of two integers (min_neg, max_neg).")
        if max_samples <= 0:
            raise ValueError("max_samples must be a positive integer.")

        self.prompt_format = prompt_format
        self.neg_samples = (min(neg_samples), max(neg_samples))
        self.max_samples = int(max_samples)
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

        all_class_texts = self._normalize_texts(labels['texts'])
        num_classes = len(all_class_texts)

        orig_cls, cls_is_numpy, orig_shape, list_wrapped_one = self._normalize_cls(
            labels['cls'])
        if len(orig_cls) == 0:
            present_classes = []
        else:
            present_classes = sorted(set(int(c)
                                     for c in orig_cls if int(c) >= 0))

        # Build positive (class_id, text) pairs
        pos_pairs: List[Tuple[int, str]] = []
        for cid in present_classes:
            if 0 <= cid < num_classes and all_class_texts[cid]:
                text_choice = random.choice(all_class_texts[cid])
                pos_pairs.append((cid, text_choice))
            else:
                # If no text available for a positive class, fall back to empty string
                pos_pairs.append((cid, ''))

        # Determine negative sampling count
        all_ids = list(range(num_classes))
        neg_candidates = [cid for cid in all_ids if cid not in present_classes]
        min_neg, max_neg = self.neg_samples
        if max_neg < 0:
            max_neg = 0
        if min_neg < 0:
            min_neg = 0
        if max_neg < min_neg:
            min_neg, max_neg = max_neg, min_neg

        # Respect max_samples capacity
        capacity_for_neg = max(self.max_samples - len(pos_pairs), 0)
        desired_neg = random.randint(min_neg, max_neg) if max_neg > 0 else 0
        n_neg = min(desired_neg, len(neg_candidates), capacity_for_neg)

        # If positives exceed max_samples, keep all positives and set negatives to 0
        if len(pos_pairs) > self.max_samples:
            n_neg = 0

        neg_pairs: List[Tuple[int, str]] = []
        if n_neg > 0 and len(neg_candidates) > 0:
            sampled_neg_ids = random.sample(neg_candidates, n_neg)
            for cid in sampled_neg_ids:
                texts_for_cid = all_class_texts[cid]
                text_choice = random.choice(
                    texts_for_cid) if texts_for_cid else ''
                neg_pairs.append((cid, text_choice))

        # Final ordering: positives first, then negatives
        final_pairs = pos_pairs + neg_pairs

        # Build formatted texts and mapping from original class id to new index
        final_texts: List[str] = []
        cid_to_new_index: Dict[int, int] = {}
        for idx, (cid, raw_text) in enumerate(final_pairs):
            cid_to_new_index[cid] = idx
            final_texts.append(self.prompt_format.format(raw_text))

        # Pad if requested
        if self.padding and len(final_texts) < self.max_samples:
            pad_needed = self.max_samples - len(final_texts)
            pad_text = self.prompt_format.format(self.padding_value)
            final_texts.extend([pad_text] * pad_needed)

        # Map original cls to new indices
        mapped_cls: List[int] = []
        for c in orig_cls:
            ci = int(c)
            if ci in cid_to_new_index:
                mapped_cls.append(cid_to_new_index[ci])
            else:
                # If a positive class somehow not included (shouldn't happen), set to -1
                mapped_cls.append(-1)

        # Restore cls to original type/shape
        if cls_is_numpy:
            if len(orig_shape) == 2 and orig_shape[1] == 1:
                new_cls = np.array(mapped_cls, dtype=int).reshape(-1, 1)
            elif len(orig_shape) == 1:
                new_cls = np.array(mapped_cls, dtype=int)
            else:
                new_cls = np.array(mapped_cls, dtype=int).reshape(
                    orig_shape[0], -1)  # best-effort
        else:
            if list_wrapped_one:
                new_cls = [[int(v)] for v in mapped_cls]
            else:
                new_cls = [int(v) for v in mapped_cls]

        updated = dict(labels)
        updated['texts'] = final_texts
        updated['cls'] = new_cls
        return updated

    @staticmethod
    def _normalize_texts(texts: Any) -> List[List[str]]:
        # texts can be:
        # - List[str]
        # - List[List[str]]
        # - np.ndarray (object or str)
        # - Dict[int, List[str]]
        # Returns: List[List[str]] where index corresponds to class id
        if isinstance(texts, dict):
            if not texts:
                return []
            max_idx = max(int(k) for k in texts.keys())
            result: List[List[str]] = [[] for _ in range(max_idx + 1)]
            for k, v in texts.items():
                idx = int(k)
                if isinstance(v, (list, tuple, np.ndarray)):
                    result[idx] = [str(x) for x in list(v)]
                else:
                    result[idx] = [str(v)]
            return result

        if isinstance(texts, np.ndarray):
            texts = texts.tolist()

        if isinstance(texts, (list, tuple)):
            if len(texts) == 0:
                return []
            # If first element is list/tuple, assume list-of-lists
            if isinstance(texts[0], (list, tuple, np.ndarray)):
                return [[str(x) for x in (list(t) if isinstance(t, (list, tuple, np.ndarray)) else [t])] for t in texts]
            else:
                # list of str
                return [[str(t)] for t in texts]

        # Fallback: single string
        return [[str(texts)]]

    @staticmethod
    def _normalize_cls(cls: Any) -> Tuple[List[int], bool, Tuple[int, ...], bool]:
        # Returns flattened list of ints, flag if numpy, original shape, and whether list was [[i], ...]
        cls_is_numpy = isinstance(cls, np.ndarray)
        list_wrapped_one = False
        orig_shape: Tuple[int, ...] = ()
        if cls_is_numpy:
            arr = cls
            orig_shape = arr.shape
            if arr.ndim == 2 and arr.shape[1] == 1:
                flat = arr.reshape(-1).tolist()
            elif arr.ndim == 1:
                flat = arr.tolist()
            else:
                flat = arr.flatten().tolist()
            flat = [int(x) for x in flat]
            return flat, True, orig_shape, False

        # list or other
        if isinstance(cls, (list, tuple)):
            if len(cls) > 0 and isinstance(cls[0], (list, tuple)) and len(cls[0]) == 1:
                list_wrapped_one = True
                flat = [int(e[0]) for e in cls]  # type: ignore[index]
            else:
                flat = [int(e) for e in cls]
            orig_shape = (len(flat),) if not list_wrapped_one else (
                len(flat), 1)
            return flat, False, orig_shape, list_wrapped_one

        # Fallback single int
        try:
            val = int(cls)
            return [val], False, (1,), False
        except Exception:
            return [], False, (0,), False
