from typing import Any, Dict


class ModelOption:
    '''A type that wraps around model options.
    Uses sentinel values (wrapped by @@@) to provide backend and model-agnostic keys for common model options.
    Create a dictionary containing model options like this:
    from mellea.backends.types import ModelOption
    model_options = { ModelOption.TEMPERATURE : 0.0, ModelOption.SYSTEM_PROMPT : "You are a helpful assistant" }
    '''

    # Sentinel keys
    TEMPERATURE = "@@@TEMPERATURE@@@"
    SYSTEM_PROMPT = "@@@SYSTEM_PROMPT@@@"

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
        if not options:
            return {}
        if not from_to:
            return dict(options)

        source_keys = set(from_to.keys())
        result: Dict[str, Any] = {k: v for k,
                                  v in options.items() if k not in source_keys}

        for src, dst in from_to.items():
            if src not in options:
                continue
            if dst in options:
                # Destination key exists in original options; keep its original value
                result[dst] = options[dst]
            else:
                # Only set if not already set by another mapping
                if dst not in result:
                    result[dst] = options[src]
        return result

    @staticmethod
    def remove_special_keys(model_options) -> dict[str, Any]:
        def is_special(k: Any) -> bool:
            return isinstance(k, str) and k.startswith("@@@") and k.endswith("@@@")
        return {k: v for k, v in dict(model_options or {}).items() if not is_special(k)}

    @staticmethod
    def merge_model_options(persistent_opts: dict[str, Any], overwrite_opts: dict[str, Any] | None) -> dict[str, Any]:
        base = dict(persistent_opts or {})
        if overwrite_opts:
            base.update(overwrite_opts)
        return base
