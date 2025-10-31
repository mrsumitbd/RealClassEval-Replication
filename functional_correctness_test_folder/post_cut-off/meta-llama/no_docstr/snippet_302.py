
from abc import ABC, abstractmethod
from typing import Optional
from confluent_kafka import Producer, TopicPartition, ClusterMetadata


class KafkaProducerPort(ABC):
    @abstractmethod
    def produce(self, message: str | bytes) -> None:
        pass

    @abstractmethod
    def flush(self, timeout: int | None) -> None:
        pass

    @abstractmethod
    def validate_healthiness(self) -> None:
        pass

    @abstractmethod
    def list_topics(self, topic: str | None, timeout: int) -> ClusterMetadata:
        pass


class KafkaProducer(KafkaProducerPort):
    def __init__(self, bootstrap_servers: str, topic: str):
        self.producer = Producer({
            'bootstrap.servers': bootstrap_servers,
        })
        self.topic = topic

    def produce(self, message: str | bytes) -> None:
        if isinstance(message, str):
            self.producer.produce(self.topic, value=message.encode('utf-8'))
        else:
            self.producer.produce(self.topic, value=message)

    def flush(self, timeout: Optional[int]) -> None:
        self.producer.flush(timeout)

    def validate_healthiness(self) -> None:
        try:
            self.producer.list_topics(timeout=10)
        except Exception as e:
            raise Exception("Kafka producer is not healthy") from e

    def list_topics(self, topic: str | None, timeout: int) -> ClusterMetadata:
        return self.producer.list_topics(topic, timeout=timeout)


# Example usage
if __name__ == "__main__":
    kafka_producer = KafkaProducer('localhost:9092', 'test_topic')
    kafka_producer.produce('Hello, Kafka!')
    kafka_producer.flush(None)
    kafka_producer.validate_healthiness()
    metadata = kafka_producer.list_topics(None, 10)
    print(metadata.topics)
