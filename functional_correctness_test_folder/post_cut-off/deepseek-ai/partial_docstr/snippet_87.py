
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
        for i in range(len(cls)):
            class_idx = cls[i]
            class_texts = texts[class_idx]
            selected_text = random.choice(class_texts)
            formatted_text = self.prompt_format.format(selected_text)
            positive_texts.append(formatted_text)

        # Sample negative texts
        num_neg_samples = random.randint(
            self.neg_samples[0], self.neg_samples[1])
        negative_texts = []
        all_negative_classes = [i for i in range(len(texts)) if i not in cls]

        for _ in range(num_neg_samples):
            if not all_negative_classes:
                break
            neg_class = random.choice(all_negative_classes)
            neg_text = random.choice(texts[neg_class])
            formatted_neg_text = self.prompt_format.format(neg_text)
            negative_texts.append(formatted_neg_text)

        combined_texts = positive_texts + negative_texts

        # Pad if necessary
        if self.padding and len(combined_texts) < self.max_samples:
            padding_needed = self.max_samples - len(combined_texts)
            combined_texts += [self.prompt_format.format(
                self.padding_value)] * padding_needed

        # Update cls indices
        new_cls = list(range(len(positive_texts)))

        labels['cls'] = new_cls
        labels['texts'] = combined_texts
        return labels
