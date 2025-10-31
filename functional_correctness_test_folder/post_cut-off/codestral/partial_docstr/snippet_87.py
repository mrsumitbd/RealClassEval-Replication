
import random
from typing import Tuple, Dict


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
        pos_cls = cls.flatten().tolist()

        # Sample negative texts
        num_neg_samples = random.randint(
            self.neg_samples[0], self.neg_samples[1])
        neg_texts = [self.padding_value] * num_neg_samples
        neg_cls = [-1] * num_neg_samples

        # Combine positive and negative texts
        combined_texts = pos_texts + neg_texts
        combined_cls = pos_cls + neg_cls

        # Format texts
        formatted_texts = [self.prompt_format.format(
            text) for text in combined_texts]

        # Pad if necessary
        if self.padding and len(formatted_texts) < self.max_samples:
            formatted_texts += [self.padding_value] * \
                (self.max_samples - len(formatted_texts))
            combined_cls += [-1] * (self.max_samples - len(combined_cls))

        # Update labels
        labels['texts'] = formatted_texts
        labels['cls'] = combined_cls

        return labels
