
from typing import Any, Dict, Optional


class ModelOption:
    """A type that wraps around model options.
    Uses sentinel values (wrapped by @@@) to provide backend and model-agnostic keys for common model options.
    Create a dictionary containing model options like this:
    from mellea.backends.types import ModelOption
    model_options = { ModelOption.TEMPERATURE : 0.0, ModelOption.SYSTEM_PROMPT : "You are a helpful assistant" }
    """

    @staticmethod
    def replace_keys(options: Dict[str, Any], from_to: Dict[str, str]) -> Dict[str, Any]:
        """
        Returns a new dict with the keys in `options` replaced with the corresponding value for that key in `from_to`.
        If any keys already exist in `options`, don't edit the associated value.

        Example:
        >>> options = {"k1": "v1", "k2": "v2", "M1": "m1"}
        >>> from_to = {"k1": "M1", "k2": "M2"}
        >>> new_options = ModelOption.replace_keys(options, from_to)
        >>> print(new_options)
        {"M1": "m1", "M2": "v2"}
        """
        new_options: Dict[str, Any] = {}
        for key, value in options.items():
            if key in from_to:
                new_key = from_to[key]
                # Only replace if the new key is not already present in the original options
                if new_key not in options:
                    new_options[new_key] = value
                # else: skip replacing; keep the original key/value
            else:
                new_options[key] = value
        return new_options

    @staticmethod
    def remove_special_keys(model_options: Dict[str, Any]) -> Dict[str, Any]:
        """
        Removes all sentinel-valued keys (i.e., those that start with @@@).
        """
        return {k: v for k, v in model_options.items() if not k.startswith("@@@")}

    @staticmethod
    def merge_model_options(
        persistent_opts: Dict[str, Any], overwrite_opts: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Creates a new dict that contains all keys and values from persistent opts and overwrite opts.
        If there are duplicate keys, overwrite opts key value pairs will be used.
        """
        merged: Dict[str, Any] = persistent_opts.copy()
        if overwrite_opts:
            merged.update(overwrite_opts)
        return merged
