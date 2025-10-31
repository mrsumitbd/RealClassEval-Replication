from django_tenants.utils import get_public_schema_name, get_tenant_base_migrate_command_class, get_tenant_database_alias

class MigrationExecutor:
    codename = None

    def __init__(self, args, options):
        self.args = args
        self.options = options
        self.PUBLIC_SCHEMA_NAME = get_public_schema_name()
        self.TENANT_DB_ALIAS = get_tenant_database_alias()

    def run_migrations(self, tenants=None):
        raise NotImplementedError

    def run_multi_type_migrations(self, tenants):
        raise NotImplementedError