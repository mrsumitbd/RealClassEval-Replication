
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
        # Get all class indices and their texts
        # labels['cls']: (N, 1) or (N,) array-like, each value is a class index
        # labels['texts']: list of list of str, each sublist is the text(s) for that class index
        # We assume that the full set of class texts is available in labels['all_texts'] if present,
        # otherwise, we infer from the union of all texts in labels['texts'].

        # 1. Get all possible class indices and their texts
        # If 'all_texts' is present, use it. Otherwise, build from 'texts'.
        if 'all_texts' in labels:
            # all_texts: list of list of str, each sublist is the text(s) for that class index
            all_texts = labels['all_texts']
            all_classes = list(range(len(all_texts)))
        else:
            # Build all_texts from the union of all texts in labels['texts']
            # This is a fallback and assumes that all possible classes are present in the image
            all_texts = labels['texts']
            all_classes = list(range(len(all_texts)))

        # 2. Get positive class indices in this image
        # labels['cls'] is (N, 1) or (N,) array-like
        pos_cls = labels['cls']
        if hasattr(pos_cls, 'tolist'):
            pos_cls = pos_cls.tolist()
        if isinstance(pos_cls, list) and isinstance(pos_cls[0], (list, tuple)):
            pos_cls = [c[0] for c in pos_cls]
        pos_cls = list(set(pos_cls))  # unique

        # 3. Get negative class indices (those not in pos_cls)
        neg_cls = [c for c in all_classes if c not in pos_cls]

        # 4. Sample negative classes
        min_neg, max_neg = self.neg_samples
        num_neg = random.randint(min_neg, min(max_neg, len(neg_cls)))
        sampled_neg_cls = random.sample(
            neg_cls, num_neg) if num_neg > 0 else []

        # 5. Compose the sampled class indices: positive first, then negative
        sampled_cls = pos_cls + sampled_neg_cls

        # 6. If max_samples is set, limit the number of samples
        if self.max_samples is not None:
            if len(sampled_cls) > self.max_samples:
                # Always keep all positives, randomly drop negatives
                num_to_remove = len(sampled_cls) - self.max_samples
                if num_to_remove > 0 and len(sampled_neg_cls) > 0:
                    drop_neg = random.sample(sampled_neg_cls, min(
                        num_to_remove, len(sampled_neg_cls)))
                    sampled_cls = pos_cls + \
                        [c for c in sampled_neg_cls if c not in drop_neg]
                sampled_cls = sampled_cls[:self.max_samples]
            elif self.padding and len(sampled_cls) < self.max_samples:
                # Will pad later
                pass

        # 7. Build the texts list and a mapping from old class index to new index
        texts = []
        old_to_new = {}
        for i, c in enumerate(sampled_cls):
            # Use the first text for each class, or join if multiple
            class_texts = all_texts[c]
            if isinstance(class_texts, (list, tuple)):
                text = class_texts[0]
            else:
                text = class_texts
            prompt = self.prompt_format.format(text)
            texts.append(prompt)
            old_to_new[c] = i

        # 8. Padding if needed
        if self.padding and len(texts) < self.max_samples:
            num_pad = self.max_samples - len(texts)
            texts += [self.padding_value] * num_pad

        # 9. Update class indices in labels['cls'] to new indices
        # For each instance, map its class index to the new index in sampled_cls
        new_cls = []
        orig_cls = labels['cls']
        if hasattr(orig_cls, 'tolist'):
            orig_cls = orig_cls.tolist()
        if isinstance(orig_cls, list) and isinstance(orig_cls[0], (list, tuple)):
            orig_cls = [c[0] for c in orig_cls]
        for c in orig_cls:
            if c in old_to_new:
                new_cls.append(old_to_new[c])
            else:
                # This should not happen, but if it does, assign to -1
                new_cls.append(-1)
        # If original was numpy, convert back
        if hasattr(labels['cls'], 'shape'):
            import numpy as np
            new_cls = np.array(new_cls).reshape(labels['cls'].shape)
        else:
            new_cls = new_cls

        # 10. Update labels
        labels = labels.copy()
        labels['cls'] = new_cls
        labels['texts'] = texts
        labels['sampled_cls'] = sampled_cls  # Optionally, for debugging

        return labels
