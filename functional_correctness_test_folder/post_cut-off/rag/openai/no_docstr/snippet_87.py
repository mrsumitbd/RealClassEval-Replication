
import random
from typing import Tuple, Dict, Any, List
import numpy as np


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
    # A small default pool of negative class names for demonstration purposes.
    _DEFAULT_NEG_POOL = [
        "elephant", "car", "tree", "house", "bicycle", "chair", "table",
        "phone", "book", "cup", "dog", "cat", "bird", "fish", "plane",
        "train", "boat", "mountain", "river", "cloud", "sun", "moon",
        "star", "flower", "rock", "sand", "snow", "rain", "wind", "fire",
        "water", "grass", "sky", "road", "bridge", "building", "garden",
        "forest", "desert", "ocean", "city", "village", "castle", "tower",
        "bridge", "airport", "hospital", "school", "office", "museum",
        "theater", "stadium", "park", "beach", "island", "cave", "volcano",
        "lake", "pond", "hill", "valley", "canyon", "glacier", "reef",
        "bush", "leaf", "branch", "root", "seed", "flower", "fruit",
        "vegetable", "meat", "bread", "cheese", "milk", "coffee", "tea",
        "soda", "wine", "beer", "juice", "water", "oil", "butter",
        "salt", "pepper", "sugar", "honey", "jam", "jelly", "candy",
        "ice", "cake", "pie", "pasta", "rice", "noodles", "soup",
        "salad", "sandwich", "burger", "pizza", "taco", "sushi",
        "ramen", "steak", "fish", "shrimp", "crab", "lobster",
        "octopus", "clam", "mussel", "scallop", "squid", "tofu",
        "bean", "lentil", "chicken", "pork", "beef", "lamb", "turkey",
        "duck", "goose", "ham", "bacon", "sausage", "kebab", "katsu",
        "kebab", "katsu", "kebab", "katsu", "kebab", "katsu"
    ]

    def __init__(self,
                 prompt_format: str = "{}",
                 neg_samples: Tuple[int, int] = (80, 80),
                 max_samples: int = 80,
                 padding: bool = False,
                 padding_value: str = "") -> None:
        """
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
        """
        self.prompt_format = prompt_format
        self.neg_samples = neg_samples
        self.max_samples = max_samples
        self.padding = padding
        self.padding_value = padding_value

    def __call__(self, labels: Dict[str, Any]) -> Dict[str, Any]:
        """
        Randomly samples positive and negative texts and updates class indices accordingly.
        This method samples positive texts based on the existing class labels in the image, and randomly
        selects negative texts from the remaining classes. It then updates the class indices to match the
        new sampled text order.
        Args:
            labels (Dict): A dictionary containing image labels and metadata. Must include 'texts' and 'cls' keys.
        Returns:
            (Dict): Updated labels dictionary with new 'cls' and 'texts' entries.
        """
        # Extract positive texts
        raw_texts = labels.get("texts", [])
        if not isinstance(raw_texts, list):
            raise ValueError("labels['texts'] must be a list")
        # Flatten if each entry is a list of strings
        positive_texts = []
        for t in raw_texts:
            if isinstance(t, list):
                positive
