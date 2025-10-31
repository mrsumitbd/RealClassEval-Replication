from django.conf import settings

class ReadReplicaRouter:
    """
    A database router that by default, reads from the writer database,
    but can be overridden with a context manager to route all reads
    to the read-replica.

    See https://docs.djangoproject.com/en/2.2/topics/db/multi-db/#automatic-database-routing
    """

    def db_for_read(self, model, **hints):
        """
        Reads go the active reader name
        """
        return _storage.db_name if _storage.db_name in settings.DATABASES else WRITER_NAME

    def db_for_write(self, model, **hints):
        """
        Writes always go to the writer.
        """
        return WRITER_NAME

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed if both objects are
        in either the read-replica or the writer.
        """
        db_list = (READ_REPLICA_NAME, WRITER_NAME)
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        All non-auth models end up in this pool.
        """
        return True