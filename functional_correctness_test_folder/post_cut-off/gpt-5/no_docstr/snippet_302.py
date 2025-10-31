from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional, Union, TYPE_CHECKING

try:
    from confluent_kafka.admin import ClusterMetadata as _ClusterMetadata
except Exception:  # pragma: no cover - allow usage without confluent_kafka installed
    _ClusterMetadata = Any

ClusterMetadata = _ClusterMetadata


class KafkaProducerPort(ABC):
    @abstractmethod
    def produce(self, message: Union[str, bytes]) -> None:
        pass

    @abstractmethod
    def flush(self, timeout: Optional[int]) -> None:
        pass

    @abstractmethod
    def validate_healthiness(self) -> None:
        pass

    @abstractmethod
    def list_topics(self, topic: Optional[str], timeout: int) -> ClusterMetadata:
        pass
