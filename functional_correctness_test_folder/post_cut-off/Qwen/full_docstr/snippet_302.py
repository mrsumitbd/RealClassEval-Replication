
from abc import ABC, abstractmethod
from typing import Union, Optional


class ClusterMetadata:
    def __init__(self, topics: dict):
        self.topics = topics


class KafkaProducerPort(ABC):
    '''Interface for Kafka producer operations.
    This interface defines the contract for producing messages to Kafka topics.
    '''

    @abstractmethod
    def produce(self, message: Union[str, bytes]) -> None:
        '''Produces a message to the configured topic.
        Args:
            message (str | bytes): The message to produce.
        Raises:
            NotImplementedError: If the method is not implemented by the concrete class.
        '''
        raise NotImplementedError

    @abstractmethod
    def flush(self, timeout: Optional[int]) -> None:
        '''Flushes any pending messages to the broker.
        Args:
            timeout (int | None): Maximum time to wait for messages to be delivered.
                If None, wait indefinitely.
        Raises:
            NotImplementedError: If the method is not implemented by the concrete class.
        '''
        raise NotImplementedError

    @abstractmethod
    def validate_healthiness(self) -> None:
        '''Validates the health of the producer connection.
        Raises:
            NotImplementedError: If the method is not implemented by the concrete class.
        '''
        raise NotImplementedError

    @abstractmethod
    def list_topics(self, topic: Optional[str], timeout: int) -> ClusterMetadata:
        '''Lists Kafka topics.
        Args:
            topic (str | None): Specific topic to list. If None, lists all topics.
            timeout (int): Timeout in seconds for the operation.
        Returns:
            ClusterMetadata: Metadata about the Kafka cluster and topics.
        Raises:
            NotImplementedError: If the method is not implemented by the concrete class.
        '''
        raise NotImplementedError
