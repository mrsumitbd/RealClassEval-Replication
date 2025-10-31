from minio.error import S3Error
from archipy.models.errors import AlreadyExistsError, ConfigurationError, ConnectionTimeoutError, InternalError, InvalidArgumentError, NetworkError, NotFoundError, PermissionDeniedError, ResourceExhaustedError, ServiceUnavailableError, StorageError

class MinioExceptionHandlerMixin:
    """Mixin class to handle MinIO/S3 exceptions in a consistent way."""

    @classmethod
    def _handle_s3_exception(cls, exception: S3Error, operation: str) -> None:
        """Handle S3Error exceptions and map them to appropriate application errors.

        Args:
            exception: The original S3Error exception
            operation: The name of the operation that failed

        Raises:
            Various application-specific errors based on the exception type/content
        """
        error_msg = str(exception).lower()
        if 'NoSuchBucket' in str(exception):
            raise NotFoundError(resource_type='bucket') from exception
        if 'NoSuchKey' in str(exception):
            raise NotFoundError(resource_type='object') from exception
        if 'BucketAlreadyOwnedByYou' in str(exception) or 'BucketAlreadyExists' in str(exception):
            raise AlreadyExistsError(resource_type='bucket') from exception
        if 'AccessDenied' in str(exception):
            raise PermissionDeniedError(additional_data={'details': f'Permission denied for operation: {operation}'}) from exception
        if 'quota' in error_msg or 'limit' in error_msg or 'exceeded' in error_msg:
            raise ResourceExhaustedError(resource_type='storage') from exception
        if 'timeout' in error_msg:
            raise ConnectionTimeoutError(service='MinIO') from exception
        if 'unavailable' in error_msg or 'connection' in error_msg:
            raise ServiceUnavailableError(service='MinIO') from exception
        raise StorageError(additional_data={'operation': operation}) from exception

    @classmethod
    def _handle_general_exception(cls, exception: Exception, component: str) -> None:
        """Handle general exceptions by converting them to appropriate application errors.

        Args:
            exception: The original exception
            component: The component/operation name for context

        Raises:
            InternalError: A wrapped version of the original exception
        """
        raise InternalError(additional_data={'component': component}) from exception