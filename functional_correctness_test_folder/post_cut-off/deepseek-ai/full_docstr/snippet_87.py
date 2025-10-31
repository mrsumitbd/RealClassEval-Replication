
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
        cls = labels['cls']
        texts = labels['texts']

        # Process positive texts
        positive_texts = []
        for idx in cls:
            idx = int(idx)  # Ensure idx is an integer
            if idx < len(texts):
                text = texts[idx][0] if isinstance(
                    texts[idx], list) else texts[idx]
                positive_texts.append(self.prompt_format.format(text))

        # Sample negative texts
        num_neg = random.randint(self.neg_samples[0], self.neg_samples[1])
        negative_indices = random.sample(
            range(len(texts)), min(num_neg, len(texts)))
        negative_texts = [self.prompt_format.format(texts[i][0] if isinstance(
            texts[i], list) else texts[i]) for i in negative_indices]

        # Combine positive and negative texts
        all_texts = positive_texts + negative_texts

        # Update class indices
        new_cls = list(range(len(positive_texts)))

        # Pad if necessary
        if self.padding and len(all_texts) < self.max_samples:
            padding_needed = self.max_samples - len(all_texts)
            all_texts += [self.padding_value] * padding_needed

        # Truncate if exceeds max_samples
        if len(all_texts) > self.max_samples:
            all_texts = all_texts[:self.max_samples]

        labels['texts'] = all_texts
        labels['cls'] = new_cls
        return labels
