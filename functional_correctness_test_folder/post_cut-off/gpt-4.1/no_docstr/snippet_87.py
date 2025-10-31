
import random
from typing import Tuple, List, Dict


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
    '''

    def __init__(self, prompt_format: str = '{}', neg_samples: Tuple[int, int] = (80, 80), max_samples: int = 80, padding: bool = False, padding_value: str = ''):
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
        # Get all class indices and their texts
        all_cls = labels['cls']
        all_texts = labels['texts']

        # Flatten all_cls to 1D list if needed
        if hasattr(all_cls, 'flatten'):
            pos_cls = list(set([int(x) for x in all_cls.flatten()]))
        else:
            pos_cls = list(set([int(x) for x in all_cls]))

        # Map from class index to text
        # all_texts: List[List[str]] or List[str]
        if isinstance(all_texts[0], list):
            class_texts = [t[0] for t in all_texts]
        else:
            class_texts = all_texts

        num_classes = len(class_texts)
        all_indices = set(range(num_classes))

        # Positive texts and indices
        pos_indices = sorted(set(pos_cls))
        pos_texts = [class_texts[i] for i in pos_indices]

        # Negative candidates
        neg_candidates = list(all_indices - set(pos_indices))
        # How many negative samples to take
        min_neg, max_neg = self.neg_samples
        if len(neg_candidates) > 0:
            n_neg = random.randint(min_neg, min(max_neg, len(neg_candidates)))
            neg_indices = random.sample(neg_candidates, n_neg)
        else:
            neg_indices = []

        neg_texts = [class_texts[i] for i in neg_indices]

        # Combine positive and negative
        combined_indices = pos_indices + neg_indices
        combined_texts = pos_texts + neg_texts

        # If more than max_samples, randomly sample
        if len(combined_texts) > self.max_samples:
            # Always keep all positives, sample negatives
            n_neg_keep = self.max_samples - len(pos_indices)
            if n_neg_keep < 0:
                # If too many positives, randomly sample positives
                keep_pos = random.sample(
                    list(enumerate(pos_indices)), self.max_samples)
                keep_pos_indices = [i for i, _ in keep_pos]
                combined_indices = [pos_indices[i] for i in keep_pos_indices]
                combined_texts = [pos_texts[i] for i in keep_pos_indices]
            else:
                # Keep all positives, sample negatives
                if n_neg_keep > 0:
                    keep_neg = random.sample(
                        list(enumerate(neg_indices)), n_neg_keep)
                    keep_neg_indices = [i for i, _ in keep_neg]
                    final_neg_indices = [neg_indices[i]
                                         for i in keep_neg_indices]
                    final_neg_texts = [neg_texts[i] for i in keep_neg_indices]
                else:
                    final_neg_indices = []
                    final_neg_texts = []
                combined_indices = pos_indices + final_neg_indices
                combined_texts = pos_texts + final_neg_texts

        # Optionally pad
        if self.padding and len(combined_texts) < self.max_samples:
            pad_len = self.max_samples - len(combined_texts)
            combined_texts += [self.padding_value] * pad_len
            combined_indices += [-1] * pad_len  # -1 for padding

        # Build mapping from original class index to new index in combined_indices
        idx_map = {cls_idx: i for i, cls_idx in enumerate(
            combined_indices) if cls_idx != -1}

        # Update 'cls' in labels to new indices
        # If original 'cls' is 2D (e.g., (N, 1)), preserve shape
        orig_cls = labels['cls']
        if hasattr(orig_cls, 'shape') and len(orig_cls.shape) > 1:
            new_cls = []
            for row in orig_cls:
                row_new = []
                for c in row:
                    c = int(c)
                    row_new.append(idx_map.get(c, -1))
                new_cls.append(row_new)
            import numpy as np
            new_cls = np.array(new_cls, dtype=orig_cls.dtype)
        else:
            new_cls = [idx_map.get(int(c), -1) for c in orig_cls]

        # Format texts
        formatted_texts = [self.prompt_format.format(
            t) if t != self.padding_value else self.padding_value for t in combined_texts]

        # Update labels
        updated_labels = dict(labels)
        updated_labels['cls'] = new_cls
        updated_labels['texts'] = formatted_texts

        return updated_labels
