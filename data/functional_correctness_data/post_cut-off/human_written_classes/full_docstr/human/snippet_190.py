from typing import Any, Dict, List, Optional, Tuple

class ClassWithInitArgs:
    """
    Wrapper class that stores constructor arguments for deferred instantiation.
    This class is particularly useful for remote class instantiation where
    the actual construction needs to happen at a different time or location.
    """

    def __init__(self, cls, *args, **kwargs) -> None:
        """Initialize the ClassWithInitArgs instance.

        Args:
            cls: The class to be instantiated later
            *args: Positional arguments for the class constructor
            **kwargs: Keyword arguments for the class constructor
        """
        self.cls = cls
        self.args = args
        self.kwargs = kwargs
        self.fused_worker_used = False

    def __call__(self) -> Any:
        """Instantiate the stored class with the stored arguments."""
        return self.cls(*self.args, **self.kwargs)