from archipy.models.errors import ConfigurationError, ConnectionTimeoutError, InternalError, InvalidArgumentError, NetworkError, ResourceExhaustedError, ServiceUnavailableError, UnavailableError

class KafkaExceptionHandlerMixin:
    """Mixin class to handle Kafka exceptions in a consistent way."""

    @classmethod
    def _handle_kafka_exception(cls, exception: Exception, operation: str) -> None:
        """Handle Kafka exceptions and map them to appropriate application errors.

        Args:
            exception: The original exception
            operation: The name of the operation that failed

        Raises:
            Various application-specific errors based on the exception type/content
        """
        error_msg = str(exception).lower()
        if 'configuration' in error_msg:
            raise ConfigurationError(config_key='kafka') from exception
        if 'invalid' in error_msg:
            raise InvalidArgumentError(argument_name=operation) from exception
        if 'timeout' in error_msg:
            timeout = None
            if hasattr(exception, 'args') and len(exception.args) > 1:
                try:
                    timeout = int(exception.args[1])
                except (IndexError, ValueError):
                    pass
            raise ConnectionTimeoutError(service='Kafka', timeout=timeout) from exception
        if 'network' in error_msg:
            raise NetworkError(service='Kafka') from exception
        if 'unavailable' in error_msg or 'connection' in error_msg:
            raise ServiceUnavailableError(service='Kafka') from exception
        raise InternalError(additional_data={'operation': operation}) from exception

    @classmethod
    def _handle_producer_exception(cls, exception: Exception, operation: str) -> None:
        """Handle producer-specific exceptions.

        Args:
            exception: The original exception
            operation: The name of the operation that failed

        Raises:
            ResourceExhaustedError: If the producer queue is full
            Various other errors from _handle_kafka_exception
        """
        if isinstance(exception, BufferError):
            raise ResourceExhaustedError(resource_type='producer_queue') from exception
        cls._handle_kafka_exception(exception, operation)