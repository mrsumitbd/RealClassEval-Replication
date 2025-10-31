
from __future__ import annotations

from typing import Any, Dict, Mapping


class ModelOption:
    """A type that wraps around model options.
    Uses sentinel values (wrapped by @@@) to provide backend and model-agnostic keys for common model options.
    Create a dictionary containing model options like this:
    from mellea.backends.types import ModelOption
    model_options = { ModelOption.TEMPERATURE : 0.0, ModelOption.SYSTEM_PROMPT : "You are a helpful assistant" }
    """

    @staticmethod
    def replace_keys(options: Mapping[str, Any], from_to: Mapping[str, str]) -> Dict[str, Any]:
        """Returns a new dict with the keys in `options` replaced with the corresponding value for that key in `from_to`.
        If any keys already exist in `options`, don't edit the associated value.
        Example:
        >>> options = {"k1": "v1", "k2": "v2", "M1": "m1"}
        >>> from_to = {"k1": "M1", "k2": "M2"}
        >>> new_options = replace_keys(options, from_to)
        >>> print(new_options)
        ... {"M1": "m1", "M2": "v2"}
        """
        # Work on a copy to avoid mutating the original
        new_options: Dict[str, Any] = dict(options)

        for old_key, new_key in from_to.items():
            if old_key in new_options:
                # If the target key already exists, keep its value
                if new_key not in new_options:
                    new_options[new_key] = new_options[old_key]
                # Remove the old key regardless of whether we copied its value
                del new_options[old_key]

        return new_options

    @staticmethod
    def remove_special_keys(model_options: Mapping[str, Any]) -> Dict[str, Any]:
        """Removes all sentiel-valued keys (i.e., those that start with @@@)."""
        return {k: v for k, v in model_options.items() if not k.startswith("@@@")}

    @staticmethod
    def merge_model_options(
        persistent_opts: Mapping[str, Any], overwrite_opts: Mapping[str, Any] | None
    ) -> Dict[str, Any]:
        """Creates a new dict that contains all keys and values from persistent opts and overwrite opts.
        If there are duplicate keys, overwrite opts key value pairs will be used.
        """
        merged: Dict[str, Any] = dict(persistent_opts)
        if overwrite_opts:
            merged.update(overwrite_opts)
        return merged
