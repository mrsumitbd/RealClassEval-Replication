class FakeTenant:
    """
    We can't import any db model in a backend (apparently?), so this class is used
    for wrapping schema names in a tenant-like structure.
    """

    def __init__(self, schema_name, tenant_type=None):
        self.schema_name = schema_name
        self.tenant_type = tenant_type

    def get_tenant_type(self):
        return self.tenant_type