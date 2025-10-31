from abc import abstractmethod
from trinity.common.config import BufferConfig, StorageConfig
from sqlalchemy.orm import sessionmaker
import ray
from typing import Dict, List, Optional
from trinity.buffer.schema import init_engine
from trinity.utils.log import get_logger
from trinity.buffer.utils import default_storage_path, retry_session

class SQLStorage:
    """
    An Storage based on SQL Database.

    If `wrap_in_ray` in `StorageConfig` is `True`, this class will be run as a Ray Actor,
    and provide a remote interface to the local database.

    For databases that do not support multi-processing read/write (e.g. sqlite, duckdb), please
    set `wrap_in_ray` to `True`.
    """

    def __init__(self, storage_config: StorageConfig, config: BufferConfig) -> None:
        self.logger = get_logger(f'sql_{storage_config.name}', in_ray_actor=True)
        if storage_config.path is None:
            storage_config.path = default_storage_path(storage_config, config)
        self.engine, self.table_model_cls = init_engine(db_url=storage_config.path, table_name=storage_config.name, schema_type=storage_config.schema_type)
        self.logger.info(f'Init SQL storage at {storage_config.path}')
        self.session = sessionmaker(bind=self.engine)
        self.max_retry_times = storage_config.max_retry_times
        self.max_retry_interval = storage_config.max_retry_interval
        self.ref_count = 0
        self.stopped = False
        self.offset = storage_config.index

    @classmethod
    def get_wrapper(cls, storage_config: StorageConfig, config: BufferConfig):
        if storage_config.schema_type is None:
            storage_cls = SQLTaskStorage
        else:
            storage_cls = SQLExperienceStorage
        if storage_config.wrap_in_ray:
            return ray.remote(storage_cls).options(name=f'sql-{storage_config.name}', namespace=storage_config.ray_namespace or ray.get_runtime_context().namespace, get_if_exists=True, max_concurrency=5).remote(storage_config, config)
        else:
            return storage_cls(storage_config, config)

    @abstractmethod
    def write(self, data: List) -> None:
        """Write a batch of data."""

    @abstractmethod
    def read(self, batch_size: Optional[int]=None) -> List:
        """Read a batch of data."""

    def acquire(self) -> int:
        self.ref_count += 1
        return self.ref_count

    def release(self) -> int:
        self.ref_count -= 1
        if self.ref_count <= 0:
            self.stopped = True
        return self.ref_count