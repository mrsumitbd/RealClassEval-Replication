
from typing import Any, Dict


class ModelOption:
    """A type that wraps around model options.

    Uses sentinel values (wrapped by @@@) to provide backend and model-agnostic keys for common model options.

    Create a dictionary containing model options like this:

    from mellea.backends.types import ModelOption
    model_options = { ModelOption.TEMPERATURE : 0.0,
        ModelOption.SYSTEM_PROMPT : "You are a helpful assistant" }
    """

    @staticmethod
    def replace_keys(options: Dict[str, Any], from_to: Dict[str, str]) -> Dict[str, Any]:
        """Returns a new dict with the keys in `options` replaced with the corresponding value for that key in `from_to`.

        If any keys already exist in `options`, don't edit the associated value.

        Example:
