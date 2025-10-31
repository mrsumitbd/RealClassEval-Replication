import random
from typing import Tuple, List, Sequence, Any


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
        >>> labels = {"cls": [0, 1, 2], "texts": [["cat"], ["dog"], ["bird"]]}
        >>> updated_labels = loader(labels)
        >>> print(updated_labels["texts"])  # doctest: +SKIP
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
            raise TypeError("prompt_format must be a string")
        if '{}' not in prompt_format:
            raise ValueError("prompt_format must contain '{}' placeholder")
        if not (isinstance(neg_samples, (tuple, list)) and len(neg_samples) == 2):
            raise TypeError("neg_samples must be a tuple/list of (min, max)")
        nmin, nmax = int(neg_samples[0]), int(neg_samples[1])
        if nmin < 0 or nmax < 0:
            raise ValueError("neg_samples values must be non-negative")
        if max_samples <= 0:
            raise ValueError("max_samples must be a positive integer")

        self.prompt_format = prompt_format
        self.neg_samples = (min(nmin, nmax), max(nmin, nmax))
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
            >>> labels = {"cls": [0, 1, 2], "texts": [["dog"], ["cat"], ["bird"]]}
            >>> updated_labels = loader(labels)
        '''
        if not isinstance(labels, dict):
            raise TypeError("labels must be a dict")
        if 'texts' not in labels or 'cls' not in labels:
            raise KeyError("labels must contain 'texts' and 'cls' keys")

        all_class_texts = labels['texts']
        if not isinstance(all_class_texts, Sequence):
            raise TypeError(
                "'texts' must be a sequence of per-class text lists")
        num_classes = len(all_class_texts)

        # Extract cls as flat list of ints, preserving original container and shape
        orig_cls = labels['cls']
        cls_list: List[int]
        orig_shape = None
        cls_container = 'list'

        # Detect numpy/torch without hard dependency
        is_numpy = hasattr(orig_cls, 'shape') and hasattr(
            orig_cls, 'dtype') and hasattr(orig_cls, 'astype')
        is_torch = hasattr(orig_cls, 'shape') and hasattr(
            orig_cls, 'dtype') and hasattr(orig_cls, 'detach') and hasattr(orig_cls, 'cpu')

        if is_torch:
            orig_shape = tuple(orig_cls.shape)
            try:
                cls_list = [int(x) for x in orig_cls.view(-1).tolist()]
            except Exception:
                cls_list = [int(x) for x in orig_cls.reshape(-1).tolist()]
            cls_container = 'torch'
            cls_dtype = orig_cls.dtype
            cls_device = orig_cls.device
        elif is_numpy:
            import numpy as np  # local import
            orig_shape = tuple(orig_cls.shape)
            cls_list = [int(x)
                        for x in np.array(orig_cls).reshape(-1).tolist()]
            cls_container = 'numpy'
            cls_dtype = orig_cls.dtype
        else:
            # assume list-like
            try:
                flat = []

                def _flatten(x):
                    if isinstance(x, (list, tuple)):
                        for y in x:
                            _flatten(y)
                    else:
                        flat.append(int(x))
                _flatten(orig_cls)
                cls_list = flat
            except Exception:
                # last resort assume iterable of ints
                cls_list = [int(x) for x in orig_cls] if isinstance(
                    orig_cls, Sequence) else [int(orig_cls)]
            cls_container = 'list'
            # best effort original "shape" for list; no reshape on return

        # Unique positive class ids in order of first appearance
        seen = set()
        pos_classes: List[int] = []
        for cid in cls_list:
            if not isinstance(cid, int):
                cid = int(cid)
            if 0 <= cid < num_classes and cid not in seen:
                seen.add(cid)
                pos_classes.append(cid)

        # Sample positive texts (one per present class)
        pos_texts: List[str] = []
        pos_class_to_index = {}
        kept_pos_classes: List[int] = []

        # Ensure we don't exceed max_samples with positives alone
        for cid in pos_classes:
            if len(pos_texts) >= self.max_samples:
                break
            texts_for_class = all_class_texts[cid]
            if not texts_for_class:
                # skip classes without texts
                continue
            choice = random.choice(list(texts_for_class))
            pos_class_to_index[cid] = len(pos_texts)
            kept_pos_classes.append(cid)
            pos_texts.append(choice)

        # Compute how many negatives to add
        remaining_slots = max(0, self.max_samples - len(pos_texts))
        nmin, nmax = self.neg_samples
        desired_negs = random.randint(nmin, nmax) if nmax > 0 else 0
        desired_negs = max(0, desired_negs)
        # respect max_samples
        desired_negs = min(desired_negs, remaining_slots)

        # Negative class candidates: classes not in kept_pos_classes and having texts
        neg_candidates = [i for i in range(
            num_classes) if i not in kept_pos_classes and all_class_texts[i]]
        if desired_negs > len(neg_candidates):
            desired_negs = len(neg_candidates)

        selected_negs = random.sample(
            neg_candidates, desired_negs) if desired_negs > 0 else []
        neg_texts: List[str] = []
        for cid in selected_negs:
            neg_texts.append(random.choice(list(all_class_texts[cid])))

        # Compose final texts and apply prompt format
        final_texts = pos_texts + neg_texts
        if self.padding and len(final_texts) < self.max_samples:
            pad_needed = self.max_samples - len(final_texts)
            final_texts.extend([self.padding_value] * pad_needed)

        formatted_texts = [self.prompt_format.format(t) for t in final_texts]

        # Remap cls: instances of classes not in kept_pos_classes are set to -1
        mapped_cls: List[int] = []
        for cid in cls_list:
            if cid in pos_class_to_index:
                mapped_cls.append(pos_class_to_index[cid])
            else:
                mapped_cls.append(-1)  # background/unassigned

        # Restore container/shape
        if cls_container == 'torch':
            import torch
            out = torch.tensor(mapped_cls, dtype=cls_dtype, device=cls_device)
            if orig_shape is not None:
                out = out.view(*orig_shape)
            labels['cls'] = out
        elif cls_container == 'numpy':
            import numpy as np
            out = np.array(mapped_cls, dtype=getattr(orig_cls, 'dtype', None))
            if orig_shape is not None:
                out = out.reshape(orig_shape)
            labels['cls'] = out
        else:
            # list
            # no shape handling for lists
            labels['cls'] = mapped_cls if orig_shape is None else mapped_cls

        labels['texts'] = formatted_texts
        return labels
