from abc import ABC, abstractmethod


class OutputSink(ABC):
    """Abstract output sink for processed markdown text."""

    @abstractmethod
    def write(self, text: str) -> None:
        """Write text to the sink."""
        raise NotImplementedError

    @abstractmethod
    def finalize(self) -> None:
        """Finalize the output."""
        raise NotImplementedError
