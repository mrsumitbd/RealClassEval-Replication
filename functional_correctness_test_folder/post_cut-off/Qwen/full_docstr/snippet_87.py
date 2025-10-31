
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
        positive_texts = labels.get('texts', [])
        positive_classes = labels.get('cls', [])

        # Flatten the list of texts if they are nested
        positive_texts = [text[0] for text in positive_texts]

        # Generate a list of all possible classes
        all_classes = set(range(self.max_samples))
        positive_class_set = set(positive_classes)
        negative_classes = list(all_classes - positive_class_set)

        # Randomly sample negative texts
        num_neg_samples = random.randint(*self.neg_samples)
        sampled_negative_classes = random.sample(
            negative_classes, min(num_neg_samples, len(negative_classes)))

        # Create negative texts
        negative_texts = [self.prompt_format.format(
            f"negative_class_{cls}") for cls in sampled_negative_classes]

        # Combine positive and negative texts
        combined_texts = [self.prompt_format.format(
            text) for text in positive_texts] + negative_texts

        # Update class indices
        updated_classes = positive_classes + sampled_negative_classes

        # Pad if necessary
        if self.padding and len(combined_texts) < self.max_samples:
            combined_texts += [self.padding_value] * \
                (self.max_samples - len(combined_texts))
            # Assuming max_samples is a valid class index for padding
            updated_classes += [self.max_samples] * \
                (self.max_samples - len(updated_classes))

        # Ensure the output is in the correct format
        updated_labels = {
            'cls': np.array(updated_classes).reshape(-1, 1),
            'texts': combined_texts
        }

        return updated_labels
