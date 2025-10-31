from django_prometheus.db import connection_errors_total, connections_total, errors_total, execute_many_total, execute_total, query_duration_seconds

class DatabaseWrapperMixin:
    """Extends the DatabaseWrapper to count connections and cursors."""

    def get_new_connection(self, *args, **kwargs):
        connections_total.labels(self.alias, self.vendor).inc()
        try:
            return super().get_new_connection(*args, **kwargs)
        except Exception:
            connection_errors_total.labels(self.alias, self.vendor).inc()
            raise

    def create_cursor(self, name=None):
        return self.connection.cursor(factory=ExportingCursorWrapper(self.CURSOR_CLASS, self.alias, self.vendor))