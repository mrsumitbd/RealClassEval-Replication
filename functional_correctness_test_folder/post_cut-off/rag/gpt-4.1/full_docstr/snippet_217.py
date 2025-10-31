from typing import Any


class ModelOption:
    '''A type that wraps around model options.
    Uses sentinel values (wrapped by @@@) to provide backend and model-agnostic keys for common model options.
    Create a dictionary containing model options like this:
    from mellea.backends.types import ModelOption
    model_options = { ModelOption.TEMPERATURE : 0.0, ModelOption.SYSTEM_PROMPT : "You are a helpful assistant" }
    '''

    @staticmethod
    def replace_keys(options: dict, from_to: dict[str, str]) -> dict[str, Any]:
        '''Returns a new dict with the keys in `options` replaced with the corresponding value for that key in `from_to`.
        If any keys already exist in `options`, don't edit the associated value.
        Example:
        >>> options = {"k1": "v1", "k2": "v2", "M1": "m1"}
        >>> from_to = {"k1": "M1", "k2": "M2"}
        >>> new_options = replace_keys(options, from_to)
        >>> print(new_options)
        ... {"M1": "m1", "M2": "v2"}
        '''
        new_options = dict(options)
        for old_key, new_key in from_to.items():
            if old_key in new_options:
                value = new_options.pop(old_key)
                # If new_key already exists, don't overwrite its value
                if new_key not in new_options:
                    new_options[new_key] = value
        return new_options

    @staticmethod
    def remove_special_keys(model_options) -> dict[str, Any]:
        '''Removes all sentiel-valued keys (i.e., those that start with @@@).'''
        return {k: v for k, v in model_options.items() if not (isinstance(k, str) and k.startswith('@@@'))}

    @staticmethod
    def merge_model_options(persistent_opts: dict[str, Any], overwrite_opts: dict[str, Any] | None) -> dict[str, Any]:
        '''Creates a new dict that contains all keys and values from persistent opts and overwrite opts. If there are duplicate keys, overwrite opts key value pairs will be used.'''
        merged = dict(persistent_opts)
        if overwrite_opts:
            merged.update(overwrite_opts)
        return merged
