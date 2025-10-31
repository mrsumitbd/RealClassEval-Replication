
from abc import ABC, abstractmethod
from typing import Union, Optional

# The ClusterMetadata type is provided by the kafka-python library.
# Import it lazily to avoid import errors if the library is not installed.
try:
    from kafka.cluster import ClusterMetadata
except Exception:  # pragma: no cover
    # Define a minimal placeholder for type checking / documentation purposes.
    class ClusterMetadata:  # pylint: disable=too-few-public-methods
        """Placeholder for kafka.cluster.ClusterMetadata."""
        pass


class KafkaProducerPort(ABC):
    """Interface for Kafka producer operations.

    Concrete implementations must provide the ability to produce messages,
    flush pending messages, validate the health of the connection, and
    list topics in the cluster.
    """

    @abstractmethod
    def produce(self, message: Union[str, bytes]) -> None:
        """Produces a message to the configured topic.

        Args:
            message (str | bytes): The message to produce.

        Raises:
            NotImplementedError: If the method is not implemented by the concrete class.
        """
        raise NotImplementedError(
            "produce() must be implemented by subclasses")

    @abstractmethod
    def flush(self, timeout: Optional[int]) -> None:
        """Flushes any pending messages to the broker.

        Args:
            timeout (int | None): Maximum time to wait for messages to be delivered.
                If None, wait indefinitely.

        Raises:
            NotImplementedError: If the method is not implemented by the concrete class.
        """
        raise NotImplementedError("flush() must be implemented by subclasses")

    @abstractmethod
    def validate_healthiness(self) -> None:
        """Validates the health of the producer connection.

        Raises:
            NotImplementedError: If the method is not implemented by the concrete class.
        """
        raise NotImplementedError(
            "validate_healthiness() must be implemented by subclasses")

    @abstractmethod
    def list_topics(self, topic: Optional[str], timeout: int) -> ClusterMetadata:
        """Lists Kafka topics.

        Args:
            topic (str | None): Specific topic to list. If None, lists all topics.
            timeout (int): Timeout in seconds for the operation.

        Returns:
            ClusterMetadata: Metadata about the Kafka cluster and topics.

        Raises:
            NotImplementedError: If the method is not implemented by the concrete class.
        """
        raise NotImplementedError(
            "list_topics() must be implemented by subclasses")
