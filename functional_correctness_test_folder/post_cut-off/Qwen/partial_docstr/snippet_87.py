
import random
from typing import Tuple, List, Dict
import numpy as np


class RandomLoadText:
    def __init__(self, prompt_format: str = '{}', neg_samples: Tuple[int, int] = (80, 80), max_samples: int = 80, padding: bool = False, padding_value: str = ''):
        self.prompt_format = prompt_format
        self.neg_samples = neg_samples
        self.max_samples = max_samples
        self.padding = padding
        self.padding_value = padding_value

    def __call__(self, labels: dict) -> dict:
        all_classes = set(range(self.max_samples))
        positive_classes = set(labels['cls'].flatten())
        negative_classes = list(all_classes - positive_classes)

        num_neg_samples = random.randint(*self.neg_samples)
        sampled_neg_classes = random.sample(
            negative_classes, min(num_neg_samples, len(negative_classes)))

        new_classes = list(positive_classes) + sampled_neg_classes
        new_texts = [self.prompt_format.format(text[0]) for text in labels['texts']] + [
            self.prompt_format.format(f'negative_class_{cls}') for cls in sampled_neg_classes]

        if self.padding and len(new_texts) < self.max_samples:
            new_texts += [self.padding_value] * \
                (self.max_samples - len(new_texts))
            new_classes += [self.max_samples] * \
                (self.max_samples - len(new_classes))

        return {
            'cls': np.array(new_classes).reshape(-1, 1),
            'texts': new_texts
        }
