
import random
from typing import Tuple, List, Dict, Any


class RandomLoadText:
    '''
    Randomly samples positive and negative texts and updates class indices accordingly.
    This class is responsible for sampling texts from a given set of class texts, including both positive
    (present in the image) and negative (not present in the image) samples. It updates the class indices
    to reflect the sampled texts and can optionally pad the text list to a fixed length.
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
        '''
        self.prompt_format = prompt_format
        self.neg_samples = neg_samples
        self.max_samples = max_samples
        self.padding = padding
        self.padding_value = padding_value

    def __call__(self, labels: dict) -> dict:
        '''
        Randomly samples positive and negative texts and updates class indices accordingly.
        '''
        # Extract all class texts and positive class indices
        # List of list of str, e.g. [["cat"], ["dog"], ...]
        all_texts: List[List[str]] = labels['texts']
        all_classes = list(range(len(all_texts)))
        # Get positive class indices from labels['cls']
        pos_cls = labels['cls']
        if hasattr(pos_cls, 'tolist'):
            pos_cls = pos_cls.tolist()
        # Flatten if needed
        if isinstance(pos_cls, list) and len(pos_cls) > 0 and isinstance(pos_cls[0], list):
            pos_cls = [x[0] for x in pos_cls]
        pos_cls = list(set(pos_cls))
        # Get positive texts and their indices
        pos_indices = pos_cls
        pos_texts = [all_texts[i][0] for i in pos_indices]
        # Get negative class indices
        neg_indices = [i for i in all_classes if i not in pos_indices]
        # Determine number of negative samples
        min_neg, max_neg = self.neg_samples
        if len(neg_indices) == 0:
            sampled_neg_indices = []
        else:
            num_neg = random.randint(min_neg, min(max_neg, len(neg_indices)))
            sampled_neg_indices = random.sample(neg_indices, num_neg)
        # Compose new text list: positive first, then negative
        sampled_indices = pos_indices + sampled_neg_indices
        sampled_texts = [all_texts[i][0] for i in sampled_indices]
        # Apply prompt format
        formatted_texts = [self.prompt_format.format(t) for t in sampled_texts]
        # If max_samples is set, limit or pad
        if self.max_samples is not None:
            if len(formatted_texts) > self.max_samples:
                formatted_texts = formatted_texts[:self.max_samples]
                sampled_indices = sampled_indices[:self.max_samples]
            elif self.padding and len(formatted_texts) < self.max_samples:
                pad_count = self.max_samples - len(formatted_texts)
                formatted_texts += [self.prompt_format.format(
                    self.padding_value)] * pad_count
                sampled_indices += [-1] * pad_count  # -1 for padded classes
        # Build mapping from old class index to new index in sampled_indices
        idx_map = {old_idx: new_idx for new_idx, old_idx in enumerate(
            sampled_indices) if old_idx in pos_indices}
        # Update labels['cls'] to new indices
        orig_cls = labels['cls']
        if hasattr(orig_cls, 'tolist'):
            orig_cls = orig_cls.tolist()
        # Flatten if needed
        if isinstance(orig_cls, list) and len(orig_cls) > 0 and isinstance(orig_cls[0], list):
            orig_cls = [x[0] for x in orig_cls]
        new_cls = []
        for c in orig_cls:
            if c in idx_map:
                new_cls.append(idx_map[c])
            else:
                new_cls.append(-1)  # Should not happen for positive classes
        # If original was numpy, convert back
        try:
            import numpy as np
            if isinstance(labels['cls'], np.ndarray):
                new_cls = np.array(new_cls).reshape(labels['cls'].shape)
        except ImportError:
            pass
        # Update labels
        labels = labels.copy()
        labels['texts'] = formatted_texts
        labels['cls'] = new_cls
        return labels
