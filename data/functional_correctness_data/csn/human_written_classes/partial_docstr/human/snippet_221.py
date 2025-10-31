from django.core.exceptions import ValidationError
from django_tenants.utils import schema_exists
from django.conf import settings
from django.db import connection, transaction

class CloneSchema:

    def _create_clone_schema_function(self):
        """
        Creates a postgres function `clone_schema` that copies a schema and its
        contents. Will replace any existing `clone_schema` functions owned by the
        `postgres` superuser.
        """
        cursor = connection.cursor()
        db_user = settings.DATABASES['default'].get('USER', None) or 'postgres'
        cursor.execute(CLONE_SCHEMA_FUNCTION.format(db_user=db_user))
        cursor.close()

    def clone_schema(self, base_schema_name, new_schema_name, clone_mode='DATA', set_connection=True):
        """
        Creates a new schema `new_schema_name` as a clone of an existing schema
        `old_schema_name`.
        """
        if set_connection:
            connection.set_schema_to_public()
        cursor = connection.cursor()
        self._create_clone_schema_function()
        transaction.commit()
        if schema_exists(new_schema_name):
            raise ValidationError('New schema name already exists')
        sql = 'SELECT clone_schema(%(base_schema)s, %(new_schema)s, %(clone_mode)s)'
        cursor.execute(sql, {'base_schema': base_schema_name, 'new_schema': new_schema_name, 'clone_mode': clone_mode})
        cursor.close()