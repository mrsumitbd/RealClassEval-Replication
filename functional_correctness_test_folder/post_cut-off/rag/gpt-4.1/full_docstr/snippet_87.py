import random
from typing import Tuple, List, Dict, Any


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
    Examples:
        >>> loader = RandomLoadText(prompt_format="Object: {}", neg_samples=(5, 10), max_samples=20)
        >>> labels = {"cls": [0, 1, 2], "texts": [["cat"], ["dog"], ["bird"]], "instances": [...]}
        >>> updated_labels = loader(labels)
        >>> print(updated_labels["texts"])
        ['Object: cat', 'Object: dog', 'Object: bird', 'Object: elephant', 'Object: car']
    '''

    def __init__(self, prompt_format: str = '{}', neg_samples: Tuple[int, int] = (80, 80), max_samples: int = 80, padding: bool = False, padding_value: str = ''):
        '''
        Initializes the RandomLoadText class for randomly sampling positive and negative texts.
        This class is designed to randomly sample positive texts and negative texts, and update the class
        indices accordingly to the number of samples. It can be used for text-based object detection tasks.
        Args:
            prompt_format (str): Format string for the prompt. Default is '{}'. The format string should
                contain a single pair of curly braces {} where the text will be inserted.
            neg_samples (Tuple[int, int]): A range to randomly sample negative texts. The first integer
                specifies the minimum number of negative samples, and the second integer specifies the
                maximum. Default is (80, 80).
            max_samples (int): The maximum number of different text samples in one image. Default is 80.
            padding (bool): Whether to pad texts to max_samples. If True, the number of texts will always
                be equal to max_samples. Default is False.
            padding_value (str): The padding text to use when padding is True. Default is an empty string.
        Attributes:
            prompt_format (str): The format string for the prompt.
            neg_samples (Tuple[int, int]): The range for sampling negative texts.
            max_samples (int): The maximum number of text samples.
            padding (bool): Whether padding is enabled.
            padding_value (str): The value used for padding.
        Examples:
            >>> random_load_text = RandomLoadText(prompt_format="Object: {}", neg_samples=(50, 100), max_samples=120)
            >>> random_load_text.prompt_format
            'Object: {}'
            >>> random_load_text.neg_samples
            (50, 100)
            >>> random_load_text.max_samples
            120
        '''
        self.prompt_format = prompt_format
        self.neg_samples = neg_samples
        self.max_samples = max_samples
        self.padding = padding
        self.padding_value = padding_value

    def __call__(self, labels: dict) -> dict:
        '''
        Randomly samples positive and negative texts and updates class indices accordingly.
        This method samples positive texts based on the existing class labels in the image, and randomly
        selects negative texts from the remaining classes. It then updates the class indices to match the
        new sampled text order.
        Args:
            labels (Dict): A dictionary containing image labels and metadata. Must include 'texts' and 'cls' keys.
        Returns:
            (Dict): Updated labels dictionary with new 'cls' and 'texts' entries.
        Examples:
            >>> loader = RandomLoadText(prompt_format="A photo of {}", neg_samples=(5, 10), max_samples=20)
            >>> labels = {"cls": np.array([[0], [1], [2]]), "texts": [["dog"], ["cat"], ["bird"]]}
            >>> updated_labels = loader(labels)
        '''
        # Get all class texts and their indices
        all_texts = labels.get('all_texts', None)
        if all_texts is None:
            # If not provided, use the unique texts in labels['texts']
            # Flatten and deduplicate
            all_texts = []
            for t in labels['texts']:
                if isinstance(t, (list, tuple)):
                    for s in t:
                        if s not in all_texts:
                            all_texts.append(s)
                else:
                    if t not in all_texts:
                        all_texts.append(t)
        else:
            # all_texts is a list of all possible class texts
            all_texts = list(all_texts)

        # Map: text -> class index
        text2cls = {str(t): i for i, t in enumerate(all_texts)}

        # Get positive class indices and texts
        pos_cls = labels['cls']
        if hasattr(pos_cls, 'tolist'):
            pos_cls = pos_cls.tolist()
        if isinstance(pos_cls, list) and len(pos_cls) > 0 and isinstance(pos_cls[0], (list, tuple)):
            pos_cls = [c[0] for c in pos_cls]
        pos_cls = list(pos_cls)
        pos_texts = []
        for idx in pos_cls:
            # Find the text for this class index
            if 'texts' in labels:
                # labels['texts'] is a list of lists, each list for a class
                if isinstance(labels['texts'][idx], (list, tuple)):
                    pos_texts.append(str(labels['texts'][idx][0]))
                else:
                    pos_texts.append(str(labels['texts'][idx]))
            else:
                # fallback: use all_texts
                pos_texts.append(str(all_texts[idx]))

        # Get negative class indices and texts
        all_indices = set(range(len(all_texts)))
        pos_indices = set()
        for t in pos_texts:
            if t in text2cls:
                pos_indices.add(text2cls[t])
        neg_indices = list(all_indices - pos_indices)
        neg_texts = [all_texts[i] for i in neg_indices]

        # How many negative samples to draw
        min_neg, max_neg = self.neg_samples
        if min_neg == max_neg:
            num_neg = min_neg
        else:
            num_neg = random.randint(min_neg, max_neg)
        # Limit by available negatives
        num_neg = min(num_neg, len(neg_texts))

        # Sample negative texts
        sampled_neg_texts = random.sample(
            neg_texts, num_neg) if num_neg > 0 else []

        # Compose the final text list: positives first, then negatives
        sampled_texts = pos_texts + sampled_neg_texts

        # If max_samples is set, limit or pad
        if self.max_samples is not None:
            if len(sampled_texts) > self.max_samples:
                sampled_texts = sampled_texts[:self.max_samples]
            elif self.padding and len(sampled_texts) < self.max_samples:
                sampled_texts = sampled_texts + \
                    [self.padding_value] * \
                    (self.max_samples - len(sampled_texts))

        # Format texts
        formatted_texts = [self.prompt_format.format(t) for t in sampled_texts]

        # Build new class indices: for each positive, its new index in the sampled_texts
        new_cls = []
        for t in pos_texts:
            try:
                idx = sampled_texts.index(t)
            except ValueError:
                idx = -1
            new_cls.append(idx)
        # If original cls was a numpy array, return as numpy array
        if hasattr(labels['cls'], 'shape'):
            import numpy as np
            new_cls = np.array(new_cls).reshape(labels['cls'].shape)
        else:
            new_cls = [[i] for i in new_cls]

        # Update labels
        new_labels = dict(labels)
        new_labels['cls'] = new_cls
        new_labels['texts'] = formatted_texts
        return new_labels
