
from abc import ABC, abstractmethod
from typing import Optional

from confluent_kafka import Producer, KafkaException
from confluent_kafka.admin import ClusterMetadata


class KafkaProducerPort(ABC):
    """Interface for Kafka producer operations.
    This interface defines the contract for producing messages to Kafka topics.
    """

    @abstractmethod
    def produce(self, message: str | bytes) -> None:
        """Produces a message to the configured topic.
        Args:
            message (str | bytes): The message to produce.
        Raises:
            NotImplementedError: If the method is not implemented by the concrete class.
        """
        pass

    @abstractmethod
    def flush(self, timeout: Optional[int]) -> None:
        """Flushes any pending messages to the broker.
        Args:
            timeout (int | None): Maximum time to wait for messages to be delivered.
                If None, wait indefinitely.
        Raises:
            NotImplementedError: If the method is not implemented by the concrete class.
        """
        pass

    @abstractmethod
    def validate_healthiness(self) -> None:
        """Validates the health of the producer connection.
        Raises:
            NotImplementedError: If the method is not implemented by the concrete class.
        """
        pass

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
        pass


class KafkaProducer(KafkaProducerPort):
    """Concrete implementation of KafkaProducerPort using confluent_kafka."""

    def __init__(self, config: dict, topic: str):
        """
        Args:
            config (dict): Producer configuration dictionary.
            topic (str): Default topic to produce messages to.
        """
        self._topic = topic
        self._producer = Producer(config)

    def produce(self, message: str | bytes) -> None:
        if isinstance(message, str):
            message = message.encode("utf-8")
        try:
            self._producer.produce(self._topic, message)
        except KafkaException as exc:
            raise RuntimeError(f"Failed to produce message: {exc}") from exc

    def flush(self, timeout: Optional[int]) -> None:
        try:
            self._producer.flush(timeout)
        except KafkaException as exc:
            raise RuntimeError(f"Failed to flush producer: {exc}") from exc

    def validate_healthiness(self) -> None:
        """Check that the producer can fetch metadata within a short timeout."""
        try:
            self._producer.list_topics(timeout=5)
        except KafkaException as exc:
            raise RuntimeError(f"Producer health check failed: {exc}") from exc

    def list_topics(self, topic: Optional[str], timeout: int) -> ClusterMetadata:
        try:
            metadata = self._producer.list_topics(topic=topic, timeout=timeout)
            if not isinstance(metadata, ClusterMetadata):
                raise TypeError(
                    "Returned metadata is not a ClusterMetadata instance")
            return metadata
        except KafkaException as exc:
            raise RuntimeError(f"Failed to list topics: {exc}") from exc
