
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
            text = texts[idx]
            if isinstance(text, list):
                text = random.choice(text)
            positive_texts.append(self.prompt_format.format(text))

        # Sample negative texts
        num_neg = random.randint(self.neg_samples[0], self.neg_samples[1])
        negative_indices = set(range(len(texts))) - set(cls.flatten().tolist())
        negative_indices = list(negative_indices)
        sampled_neg_indices = random.sample(
            negative_indices, min(num_neg, len(negative_indices)))
        negative_texts = []
        for idx in sampled_neg_indices:
            text = texts[idx]
            if isinstance(text, list):
                text = random.choice(text)
            negative_texts.append(self.prompt_format.format(text))

        # Combine positive and negative texts
        all_texts = positive_texts + negative_texts

        # Update cls indices
        new_cls = [[i] for i in range(len(positive_texts))]

        # Pad if necessary
        if self.padding and len(all_texts) < self.max_samples:
            padding_needed = self.max_samples - len(all_texts)
            all_texts += [self.prompt_format.format(
                self.padding_value)] * padding_needed

        # Truncate if exceeds max_samples
        if len(all_texts) > self.max_samples:
            all_texts = all_texts[:self.max_samples]

        labels['texts'] = all_texts
        labels['cls'] = new_cls
        return labels
