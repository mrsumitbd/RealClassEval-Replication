
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Union

from confluent_kafka import Producer, KafkaException, KafkaError
from confluent_kafka.admin import ClusterMetadata


class KafkaProducerPort(ABC):
    """
    Abstract base class defining the interface for a Kafka producer.
    """

    @abstractmethod
    def produce(self, message: Union[str, bytes]) -> None:
        """Send a message to Kafka."""
        pass

    @abstractmethod
    def flush(self, timeout: Optional[int]) -> None:
        """Flush all buffered messages."""
        pass

    @abstractmethod
    def validate_healthiness(self) -> None:
        """Validate that the producer can communicate with the cluster."""
        pass

    @abstractmethod
    def list_topics(self, topic: Optional[str], timeout: int) -> ClusterMetadata:
        """Retrieve metadata for the specified topic or all topics."""
        pass


class ConfluentKafkaProducer(KafkaProducerPort):
    """
    Concrete implementation of KafkaProducerPort using confluent_kafka.
    """

    def __init__(self, config: dict):
        """
        Initialize the producer with the given configuration.

        :param config: Dictionary of configuration options for the Producer.
        """
        self._producer = Producer(config)

    def produce(self, message: Union[str, bytes]) -> None:
        """
        Produce a message to the default topic specified in the configuration.

        :param message: The message to send. Can be a string or bytes.
        :raises KafkaException: If the message cannot be queued.
        """
        # The default topic must be provided in the config under 'default_topic'
        default_topic = self._producer.config.get("default_topic")
        if not default_topic:
            raise ValueError(
                "Producer configuration must include 'default_topic'")

        # Ensure message is bytes
        if isinstance(message, str):
            message_bytes = message.encode("utf-8")
        else:
            message_bytes = message

        try:
            self._producer.produce(default_topic, message_bytes)
        except BufferError as e:
            # BufferError is raised when the local queue is full
            raise KafkaException(KafkaError(e)) from e
        except Exception as e:
            raise KafkaException(KafkaError(e)) from e

    def flush(self, timeout: Optional[int]) -> None:
        """
        Flush all messages in the producer's queue.

        :param timeout: Maximum time in seconds to wait for flush. If None, block indefinitely.
        """
        # confluent_kafka's flush accepts timeout in seconds
        self._producer.flush(timeout)

    def validate_healthiness(self) -> None:
        """
        Validate that the producer can communicate with the cluster by fetching metadata.

        :raises KafkaException: If metadata cannot be retrieved.
        """
        try:
            # Attempt to fetch metadata for all topics with a short timeout
            self._producer.list_topics(timeout=5)
        except Exception as e:
            raise KafkaException(KafkaError(e)) from e

    def list_topics(self, topic: Optional[str], timeout: int) -> ClusterMetadata:
        """
        Retrieve metadata for the specified topic or all topics.

        :param topic: Topic name to query. If None, all topics are returned.
        :param timeout: Timeout in seconds for the metadata request.
        :return: ClusterMetadata object containing topic information.
        :raises KafkaException: If metadata cannot be retrieved.
        """
        try:
            metadata = self._producer.list_topics(topic=topic, timeout=timeout)
            if not isinstance(metadata, ClusterMetadata):
                raise KafkaException(KafkaError(
                    "Invalid metadata type returned"))
            return metadata
        except Exception as e:
            raise KafkaException(KafkaError(e)) from e
