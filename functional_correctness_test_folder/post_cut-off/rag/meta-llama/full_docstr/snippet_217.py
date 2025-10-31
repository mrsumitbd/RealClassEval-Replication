
from typing import Any, Dict


class ModelOption:
    """A type that wraps around model options.

    Uses sentinel values (wrapped by @@@) to provide backend and model-agnostic keys for common model options.

    Create a dictionary containing model options like this:
