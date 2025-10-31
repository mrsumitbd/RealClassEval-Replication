
from abc import ABC, abstractmethod
from typing import Union

# The type used for the return value of `list_topics`.  Importing it lazily
# avoids pulling in the whole Kafka client unless this module is actually
# used.
try:
    from kafka.cluster import ClusterMetadata
except Exception:  # pragma: no cover
    # In environments where the Kafka client is not available we still
    # provide a minimal placeholder so that type checking and IDEs can
    # resolve the name.
    class ClusterMetadata:  # type: ignore
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
            NotImplementedError: If the method is not implemented by the
                concrete class.
        """
        raise NotImplementedError

    @abstractmethod
    def flush(self, timeout: Union[int, None]) -> None:
        """Flushes any pending messages to the broker.

        Args:
            timeout (int | None): Maximum time to wait for messages to be
                delivered. If None, wait indefinitely.

        Raises:
            NotImplementedError: If the method is not implemented by the
                concrete class.
        """
        raise NotImplementedError

    @abstractmethod
    def validate_healthiness(self) -> None:
        """Validates the health of the producer connection.

        Raises:
            NotImplementedError: If the method is not implemented by the
                concrete class.
        """
        raise NotImplementedError

    @abstractmethod
    def list_topics(self, topic: Union[str, None], timeout: int) -> ClusterMetadata:
        """Lists Kafka topics.

        Args:
            topic (str | None): Specific topic to list. If None, lists all
                topics.
            timeout (int): Timeout in seconds for the operation.

        Returns:
            ClusterMetadata: Metadata about the Kafka cluster and topics.

        Raises:
            NotImplementedError: If the method is not implemented by the
                concrete class.
        """
        raise NotImplementedError
