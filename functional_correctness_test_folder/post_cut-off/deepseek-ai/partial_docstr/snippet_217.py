
class ModelOption:
    '''A type that wraps around model options.
    Uses sentinel values (wrapped by @@@) to provide backend and model-agnostic keys for common model options.
    Create a dictionary containing model options like this:
    from mellea.backends.types import ModelOption
    model_options = { ModelOption.TEMPERATURE : 0.0, ModelOption.SYSTEM_PROMPT : "You are a helpful assistant" }
    '''
    @staticmethod
    def replace_keys(options: dict, from_to: dict[str, str]) -> dict[str, Any]:
        new_options = {}
        for key, value in options.items():
            if key in from_to:
                new_key = from_to[key]
                if new_key not in new_options:
                    new_options[new_key] = value
            else:
                if key not in new_options:
                    new_options[key] = value
        return new_options

    @staticmethod
    def remove_special_keys(model_options: dict[str, Any]) -> dict[str, Any]:
        return {k: v for k, v in model_options.items() if not k.startswith('@@@')}

    @staticmethod
    def merge_model_options(persistent_opts: dict[str, Any], overwrite_opts: dict[str, Any] | None) -> dict[str, Any]:
        merged = persistent_opts.copy()
        if overwrite_opts is not None:
            merged.update(overwrite_opts)
        return merged
