from redis.asyncio.retry import Retry
from urllib.parse import parse_qs, urlparse
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, List, Optional, Tuple, Union, cast

@dataclass
class RedisSettings:
    """
    No-Op class used to hold redis connection redis_settings.

    Used by :func:`arq.connections.create_pool` and :class:`arq.worker.Worker`.
    """
    host: Union[str, List[Tuple[str, int]]] = 'localhost'
    port: int = 6379
    unix_socket_path: Optional[str] = None
    database: int = 0
    username: Optional[str] = None
    password: Optional[str] = None
    ssl: bool = False
    ssl_keyfile: Optional[str] = None
    ssl_certfile: Optional[str] = None
    ssl_cert_reqs: str = 'required'
    ssl_ca_certs: Optional[str] = None
    ssl_ca_data: Optional[str] = None
    ssl_check_hostname: bool = False
    conn_timeout: int = 1
    conn_retries: int = 5
    conn_retry_delay: int = 1
    max_connections: Optional[int] = None
    sentinel: bool = False
    sentinel_master: str = 'mymaster'
    retry_on_timeout: bool = False
    retry_on_error: Optional[List[Exception]] = None
    retry: Optional[Retry] = None

    @classmethod
    def from_dsn(cls, dsn: str) -> 'RedisSettings':
        conf = urlparse(dsn)
        if conf.scheme not in {'redis', 'rediss', 'unix'}:
            raise RuntimeError('invalid DSN scheme')
        query_db = parse_qs(conf.query).get('db')
        if query_db:
            database = int(query_db[0])
        elif conf.scheme != 'unix':
            database = int(conf.path.lstrip('/')) if conf.path else 0
        else:
            database = 0
        return RedisSettings(host=conf.hostname or 'localhost', port=conf.port or 6379, ssl=conf.scheme == 'rediss', username=conf.username, password=conf.password, database=database, unix_socket_path=conf.path if conf.scheme == 'unix' else None)

    def __repr__(self) -> str:
        return 'RedisSettings({})'.format(', '.join((f'{k}={v!r}' for k, v in self.__dict__.items())))