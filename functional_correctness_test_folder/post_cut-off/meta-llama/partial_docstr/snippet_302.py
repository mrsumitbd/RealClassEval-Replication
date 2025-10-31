
from abc import ABC, abstractmethod
from typing import Union
from confluent_kafka import Producer, TopicPartition, ClusterMetadata


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
    def __init__(self, bootstrap_servers: str, topic: str, **kwargs):
        self.producer = Producer({
            'bootstrap.servers': bootstrap_servers,
            **kwargs
        })
        self.topic = topic

    def produce(self, message: Union[str, bytes]) -> None:
        if isinstance(message, str):
            message = message.encode('utf-8')
        self.producer.produce(self.topic, value=message)

    def flush(self, timeout: Union[int, None]) -> None:
        self.producer.flush(timeout)

    def validate_healthiness(self) -> None:
        try:
            self.producer.list_topics(timeout=10)
        except Exception as e:
            raise Exception("Producer is not healthy") from e

    def list_topics(self, topic: Union[str, None], timeout: int) -> ClusterMetadata:
        return self.producer.list_topics(topic, timeout=timeout)


# Example usage
if __name__ == "__main__":
    producer = ConfluentKafkaProducer('localhost:9092', 'my_topic')
    producer.produce('Hello, Kafka!')
    producer.flush(10)
    producer.validate_healthiness()
    metadata = producer.list_topics(None, 10)
    print(metadata.topics)
