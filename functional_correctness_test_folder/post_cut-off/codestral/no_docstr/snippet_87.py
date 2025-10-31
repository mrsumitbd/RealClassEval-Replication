
import random
from typing import Tuple, Dict, List


class RandomLoadText:
    def __init__(self, prompt_format: str = '{}', neg_samples: Tuple[int, int] = (80, 80), max_samples: int = 80, padding: bool = False, padding_value: str = ''):
        self.prompt_format = prompt_format
        self.neg_samples = neg_samples
        self.max_samples = max_samples
        self.padding = padding
        self.padding_value = padding_value

    def __call__(self, labels: Dict) -> Dict:
        texts = labels['texts']
        cls = labels['cls']

        # Sample positive texts
        pos_texts = [text[0] for text in texts]
        pos_cls = [c[0] for c in cls]

        # Sample negative texts
        num_neg_samples = random.randint(
            self.neg_samples[0], self.neg_samples[1])
        all_classes = set(range(self.max_samples))
        neg_classes = list(all_classes - set(pos_cls))
        neg_texts = random.sample(neg_classes, min(
            num_neg_samples, len(neg_classes)))
        neg_texts = [f"not {text}" for text in neg_texts]

        # Combine positive and negative texts
        combined_texts = pos_texts + neg_texts
        combined_cls = pos_cls + neg_texts

        # Pad if necessary
        if self.padding and len(combined_texts) < self.max_samples:
            combined_texts += [self.padding_value] * \
                (self.max_samples - len(combined_texts))
            combined_cls += [-1] * (self.max_samples - len(combined_cls))

        # Update labels
        labels['texts'] = [self.prompt_format.format(
            text) for text in combined_texts]
        labels['cls'] = combined_cls

        return labels
