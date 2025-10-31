
from abc import ABC, abstractmethod
from confluent_kafka.admin import ClusterMetadata


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
