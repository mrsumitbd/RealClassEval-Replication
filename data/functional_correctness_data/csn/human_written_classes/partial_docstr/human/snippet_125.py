from bigchaindb.backend.exceptions import ConnectionError
from itertools import repeat
import bigchaindb

class Connection:
    """Connection class interface.

    All backend implementations should provide a connection class that inherits
    from and implements this class.
    """

    def __init__(self, host=None, port=None, dbname=None, connection_timeout=None, max_tries=None, **kwargs):
        """Create a new :class:`~.Connection` instance.

        Args:
            host (str): the host to connect to.
            port (int): the port to connect to.
            dbname (str): the name of the database to use.
            connection_timeout (int, optional): the milliseconds to wait
                until timing out the database connection attempt.
                Defaults to 5000ms.
            max_tries (int, optional): how many tries before giving up,
                if 0 then try forever. Defaults to 3.
            **kwargs: arbitrary keyword arguments provided by the
                configuration's ``database`` settings
        """
        dbconf = bigchaindb.config['database']
        self.host = host or dbconf['host']
        self.port = port or dbconf['port']
        self.dbname = dbname or dbconf['name']
        self.connection_timeout = connection_timeout if connection_timeout is not None else dbconf['connection_timeout']
        self.max_tries = max_tries if max_tries is not None else dbconf['max_tries']
        self.max_tries_counter = range(self.max_tries) if self.max_tries != 0 else repeat(0)
        self._conn = None

    @property
    def conn(self):
        if self._conn is None:
            self.connect()
        return self._conn

    def run(self, query):
        """Run a query.

        Args:
            query: the query to run
        Raises:
            :exc:`~DuplicateKeyError`: If the query fails because of a
                duplicate key constraint.
            :exc:`~OperationFailure`: If the query fails for any other
                reason.
            :exc:`~ConnectionError`: If the connection to the database
                fails.
        """
        raise NotImplementedError()

    def connect(self):
        """Try to connect to the database.

        Raises:
            :exc:`~ConnectionError`: If the connection to the database
                fails.
        """
        attempt = 0
        for i in self.max_tries_counter:
            attempt += 1
            try:
                self._conn = self._connect()
            except ConnectionError as exc:
                logger.warning('Attempt %s/%s. Connection to %s:%s failed after %sms.', attempt, self.max_tries if self.max_tries != 0 else '∞', self.host, self.port, self.connection_timeout)
                if attempt == self.max_tries:
                    logger.critical('Cannot connect to the Database. Giving up.')
                    raise ConnectionError() from exc
            else:
                break