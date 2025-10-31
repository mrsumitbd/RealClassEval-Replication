
from typing import Dict, List


class ModelConfig:
    """
    Simple configuration holder for a handful of pre‑defined models.
    """

    # Class‑level registry of supported models and their basic info
    _MODEL_REGISTRY: Dict[str, Dict[str, str]] = {
        "bert-base-uncased": {
            "tokenizer": "bert-base-uncased",
            "model_path": "bert-base-uncased",
            "framework": "pytorch",
        },
        "gpt-2": {
            "tokenizer": "gpt2",
            "model_path": "gpt2",
            "framework": "pytorch",
        },
        "roberta-base": {
            "tokenizer": "roberta-base",
            "model_path": "roberta-base",
            "framework": "pytorch",
        },
    }

    def __init__(self, model_name: str):
        """
        Initialize the configuration for a specific model.

        Parameters
        ----------
        model_name : str
            The name of the model to configure. Must be one of the supported
            model names returned by :meth:`get_supported_models`.

        Raises
        ------
        ValueError
            If the supplied model name is not supported.
        """
        self.model_name = model_name
        self.model_info = self._get_model_info(model_name)

    def _get_model_info(self, model_name: str) -> Dict[str, str]:
        """
        Retrieve the configuration dictionary for a given model name.

        Parameters
        ----------
        model_name : str
            The name of the model.

        Returns
        -------
        Dict[str, str]
            A dictionary containing model configuration details.

        Raises
        ------
        ValueError
            If the model name is not found in the registry.
        """
        if model_name not in self._MODEL_REGISTRY:
            raise ValueError(
                f"Unsupported model '{model_name}'. "
                f"Supported models: {', '.join(self.get_supported_models())}"
            )
        return self._MODEL_REGISTRY[model_name]

    @classmethod
    def get_supported_models(cls) -> List[str]:
        """
        Return a list of all supported model names.

        Returns
        -------
        List[str]
            The names of all models available in the registry.
        """
        return list(cls._MODEL_REGISTRY.keys())
