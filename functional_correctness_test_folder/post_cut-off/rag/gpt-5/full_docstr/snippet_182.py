from abc import ABC, abstractmethod


class OutputSink(ABC):
    """Abstract output sink for processed markdown text."""

    @abstractmethod
    def write(self, text: str) -> None:
        """Write text to the sink."""
        raise NotImplementedError(
            "OutputSink.write must be implemented by subclasses")

    @abstractmethod
    def finalize(self) -> None:
        """Finalize the output."""
        raise NotImplementedError(
            "OutputSink.finalize must be implemented by subclasses")
