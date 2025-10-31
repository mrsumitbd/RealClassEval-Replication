
from __future__ import annotations
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
        new_options: Dict[str, Any] = dict(options)
        for old_key, new_key in from_to.items():
            if old_key in new_options:
                # Preserve existing value for new_key if it already exists
                if new_key not in new_options:
                    new_options[new_key] = new_options.pop(old_key)
                else:
                    new_options.pop(old_key)
        return new_options

    @staticmethod
    def remove_special_keys(model_options: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove keys that are sentinel values wrapped by @@@.
        Sentinel keys are expected to start and end with '@@@'.
        """
        return {
            k: v
            for k, v in model_options.items()
            if not (isinstance(k, str) and k.startswith("@@@") and k.endswith("@@@"))
        }

    @staticmethod
    def merge_model_options(
        persistent_opts: Dict[str, Any],
        overwrite_opts: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Merge persistent options with overwrite options.
        If overwrite_opts is None, return a copy of persistent_opts.
        Otherwise, overwrite or add keys from overwrite_opts into persistent_opts.
        """
        result: Dict[str, Any] = dict(persistent_opts)
        if overwrite_opts:
            result.update(overwrite_opts)
        return result
