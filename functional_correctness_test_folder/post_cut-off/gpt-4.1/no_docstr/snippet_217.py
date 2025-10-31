
from typing import Any


class ModelOption:
    '''A type that wraps around model options.
    Uses sentinel values (wrapped by @@@) to provide backend and model-agnostic keys for common model options.
    Create a dictionary containing model options like this:
    from mellea.backends.types import ModelOption
    model_options = { ModelOption.TEMPERATURE : 0.0, ModelOption.SYSTEM_PROMPT : "You are a helpful assistant" }
    '''

    # Sentinel values for common model options
    TEMPERATURE = "@@@TEMPERATURE@@@"
    SYSTEM_PROMPT = "@@@SYSTEM_PROMPT@@@"
    MAX_TOKENS = "@@@MAX_TOKENS@@@"
    TOP_P = "@@@TOP_P@@@"
    TOP_K = "@@@TOP_K@@@"
    STOP_SEQUENCES = "@@@STOP_SEQUENCES@@@"
    PRESENCE_PENALTY = "@@@PRESENCE_PENALTY@@@"
    FREQUENCY_PENALTY = "@@@FREQUENCY_PENALTY@@@"
    N = "@@@N@@@"
    SEED = "@@@SEED@@@"
    USER = "@@@USER@@@"
    TOOLS = "@@@TOOLS@@@"
    TOOL_CHOICE = "@@@TOOL_CHOICE@@@"
    RESPONSE_FORMAT = "@@@RESPONSE_FORMAT@@@"
    FUNCTION_CALL = "@@@FUNCTION_CALL@@@"
    FUNCTIONS = "@@@FUNCTIONS@@@"
    LOGIT_BIAS = "@@@LOGIT_BIAS@@@"
    LOGPROBS = "@@@LOGPROBS@@@"
    STREAM = "@@@STREAM@@@"
    ECHO = "@@@ECHO@@@"
    BEST_OF = "@@@BEST_OF@@@"
    LOG_LEVEL = "@@@LOG_LEVEL@@@"
    JSON_MODE = "@@@JSON_MODE@@@"

    @staticmethod
    def replace_keys(options: dict, from_to: dict[str, str]) -> dict[str, Any]:
        '''Returns a new dict with the keys in `options` replaced with the corresponding value for that key in `from_to`.
        If any keys already exist in `options`, don't edit the associated value.
        '''
        new_options = {}
        for k, v in options.items():
            if k in from_to:
                new_key = from_to[k]
                # If the new key already exists in options, use its value, not v
                if new_key in options:
                    new_options[new_key] = options[new_key]
                else:
                    new_options[new_key] = v
            else:
                new_options[k] = v
        return new_options

    @staticmethod
    def remove_special_keys(model_options) -> dict[str, Any]:
        '''Removes all keys that are sentinel values (i.e., start and end with "@@@")'''
        return {k: v for k, v in model_options.items() if not (isinstance(k, str) and k.startswith("@@@") and k.endswith("@@@"))}

    @staticmethod
    def merge_model_options(persistent_opts: dict[str, Any], overwrite_opts: dict[str, Any] | None) -> dict[str, Any]:
        '''Returns a new dict with persistent_opts updated with overwrite_opts (if not None).'''
        merged = dict(persistent_opts) if persistent_opts is not None else {}
        if overwrite_opts:
            merged.update(overwrite_opts)
        return merged
