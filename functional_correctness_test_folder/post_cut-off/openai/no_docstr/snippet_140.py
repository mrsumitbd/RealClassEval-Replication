
from typing import Union, List, Dict, Any
import torch
from transformers import AutoModel, AutoTokenizer


class QwenEmbedding:
    """
    A simple wrapper around a Qwen model to produce sentence embeddings.
    """

    def __init__(self, config: Union[Dict[str, Any], None] = None):
        """
        Initialize the QwenEmbedding instance.

        Parameters
        ----------
        config : dict or None, optional
            Configuration dictionary. Supported keys:
                - model_name : str, default 'Qwen/Qwen-7B-
