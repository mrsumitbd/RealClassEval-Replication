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
        result: dict[str, Any] = dict(options)

        # For each mapping, if the target key already exists, keep it as-is.
        # Otherwise, if the source key exists, move its value to the target key.
        for src_key, dst_key in from_to.items():
            if dst_key in result:
                continue
            if src_key in result:
                result[dst_key] = result[src_key]

        # Remove all source keys after moving/replacing
        for src_key in from_to.keys():
            if src_key in result:
                del result[src_key]

        return result

    @staticmethod
    def remove_special_keys(model_options) -> dict[str, Any]:
        '''Removes all sentiel-valued keys (i.e., those that start with @@@).'''
        if model_options is None:
            return {}
        return {k: v for k, v in dict(model_options).items() if not (isinstance(k, str) and k.startswith('@@@'))}

    @staticmethod
    def merge_model_options(persistent_opts: dict[str, Any], overwrite_opts: dict[str, Any] | None) -> dict[str, Any]:
        result: dict[str, Any] = dict(persistent_opts or {})
        if overwrite_opts:
            result.update(overwrite_opts)
        return result
