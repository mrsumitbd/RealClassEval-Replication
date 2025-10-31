
from __future__ import annotations

from typing import List, Optional

from confluent_kafka.admin import (
    AdminClient,
    ClusterMetadata,
    DeleteTopics,
    NewTopic,
)
from confluent_kafka import KafkaException


class KafkaAdminPort:
    """
    Concrete implementation of the Kafka admin interface.

    Parameters
    ----------
    bootstrap_servers : str | list[str]
        Bootstrap server(s) for the Kafka cluster.
    client_config : dict, optional
        Additional configuration for the AdminClient.
    """

    def __init__(
        self,
        bootstrap_servers: str | List[str],
        client_config: Optional[dict] = None,
    ) -> None:
        config = {"bootstrap.servers": bootstrap_servers}
        if client_config:
            config.update(client_config)
        self._admin_client = AdminClient(config)

    def create_topic(
        self,
        topic: str,
        num_partitions: int = 1,
        replication_factor: int = 1,
    ) -> None:
        """
        Creates a new Kafka topic.

        Parameters
        ----------
        topic : str
            Name of the topic to create.
        num_partitions : int, optional
            Number of partitions for the topic. Defaults to 1.
        replication_factor : int, optional
            Replication factor for the topic. Defaults to 1.

        Raises
        ------
        KafkaException
            If the topic creation fails.
        """
        new_topic = NewTopic(
            topic,
            num_partitions=num_partitions,
            replication_factor=replication_factor,
        )
        futures = self._admin_client.create_topics([new_topic])
        # Wait for the result
        for t, f in futures.items():
            try:
                f.result(timeout=10)
            except KafkaException as exc:
                raise KafkaException(
                    f"Failed to create topic '{t}': {exc}"
                ) from exc

    def delete_topic(self, topics: List[str]) -> None:
        """
        Deletes one or more Kafka topics.

        Parameters
        ----------
        topics : list[str]
            List of topic names to delete.

        Raises
        ------
        KafkaException
            If the topic deletion fails.
        """
        delete_futures = self._admin_client.delete_topics(topics)
        for t, f in delete_futures.items():
            try:
                f.result(timeout=10)
            except KafkaException as exc:
                raise KafkaException(
                    f"Failed to delete topic '{t}': {exc}"
                ) from exc

    def list_topics(
        self,
        topic: Optional[str] = None,
        timeout: int = 1,
    ) -> ClusterMetadata:
        """
        Lists Kafka topics.

        Parameters
        ----------
        topic : str | None, optional
            Specific topic to list. If None, lists all topics.
        timeout : int, optional
            Timeout in seconds for the operation. Defaults to 1.

        Returns
        -------
        ClusterMetadata
            Metadata about the Kafka cluster and topics.

        Raises
        ------
        KafkaException
            If the operation fails.
        """
        try:
            metadata = self._admin_client.list_topics(topic, timeout=timeout)
            return metadata
        except KafkaException as exc:
            raise KafkaException(f"Failed to list topics: {exc}") from exc
