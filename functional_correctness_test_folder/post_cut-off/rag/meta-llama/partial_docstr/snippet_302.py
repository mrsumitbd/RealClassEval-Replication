
from abc import ABC, abstractmethod
from confluent_kafka import Producer, TopicPartition, ClusterMetadata
from typing import Union


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
        pass

    @abstractmethod
    def flush(self, timeout: Union[int, None]) -> None:
        '''Flushes any pending messages to the broker.
        Args:
            timeout (int | None): Maximum time to wait for messages to be delivered.
                If None, wait indefinitely.
        Raises:
            NotImplementedError: If the method is not implemented by the concrete class.
        '''
        pass

    @abstractmethod
    def validate_healthiness(self) -> None:
        '''Validates the health of the producer connection.
        Raises:
            NotImplementedError: If the method is not implemented by the concrete class.
        '''
        pass

    @abstractmethod
    def list_topics(self, topic: Union[str, None], timeout: int) -> ClusterMetadata:
        '''Lists Kafka topics.
        Args:
            topic (str | None): Specific topic to list. If None, lists all topics.
            timeout (int): Timeout in seconds for the operation.
        Returns:
            ClusterMetadata: Metadata about the Kafka cluster and topics.
        Raises:
            NotImplementedError: If the method is not implemented by the concrete class.
        '''
        pass


class ConfluentKafkaProducer(KafkaProducerPort):
    '''Implementation of KafkaProducerPort using Confluent Kafka library.'''

    def __init__(self, bootstrap_servers: str, topic: str, **kwargs):
        '''Initializes the Confluent Kafka producer.

        Args:
            bootstrap_servers (str): Comma-separated list of Kafka bootstrap servers.
            topic (str): Default topic to produce messages to.
            **kwargs: Additional keyword arguments to pass to the Confluent Kafka Producer.
        '''
        self._producer = Producer({
            'bootstrap.servers': bootstrap_servers,
            **kwargs
        })
        self._topic = topic

    def produce(self, message: Union[str, bytes]) -> None:
        '''Produces a message to the configured topic.

        Args:
            message (str | bytes): The message to produce.
        '''
        if isinstance(message, str):
            message = message.encode('utf-8')
        self._producer.produce(self._topic, value=message)

    def flush(self, timeout: Union[int, None]) -> None:
        '''Flushes any pending messages to the broker.

        Args:
            timeout (int | None): Maximum time to wait for messages to be delivered.
                If None, wait indefinitely.
        '''
        self._producer.flush(timeout)

    def validate_healthiness(self) -> None:
        '''Validates the health of the producer connection.'''
        # Confluent Kafka producer does not have an explicit health check method.
        # We can try to produce a dummy message to test the connection.
        try:
            self._producer.produce(self._topic, value=b'health_check')
            self._producer.flush(1)
        except Exception as e:
            raise RuntimeError('Producer is not healthy') from e

    def list_topics(self, topic: Union[str, None], timeout: int) -> ClusterMetadata:
        '''Lists Kafka topics.

        Args:
            topic (str | None): Specific topic to list. If None, lists all topics.
            timeout (int): Timeout in seconds for the operation.

        Returns:
            ClusterMetadata: Metadata about the Kafka cluster and topics.
        '''
        return self._producer.list_topics(topic, timeout)
