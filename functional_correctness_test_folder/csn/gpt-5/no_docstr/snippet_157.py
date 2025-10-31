class HashMixin:
    def __init__(self, original=None, *args, **kwargs):
        self.original = original
        try:
            super().__init__(*args, **kwargs)
        except Exception:
            pass

    def pre_save(self, model_instance, add):
        import hashlib

        if not self.original:
            return getattr(model_instance, getattr(self, "attname", None), None)

        source = getattr(model_instance, self.original, None)
        if source is None:
            return None

        if isinstance(source, bytes):
            data = source
        else:
            data = str(source).encode("utf-8")

        hashed = hashlib.sha256(data).hexdigest()

        attname = getattr(self, "attname", None)
        if attname:
            try:
                setattr(model_instance, attname, hashed)
            except Exception:
                pass

        return hashed

    def get_placeholder(self, value=None, compiler=None, connection=None):
        conn = connection or getattr(compiler, "connection", None)
        sql = self.get_encrypt_sql(conn)
        if "%s" in sql:
            return sql
        return "%s"

    def get_encrypt_sql(self, connection):
        vendor = getattr(connection, "vendor", None)

        if vendor == "postgresql":
            return "encode(digest(%s, 'sha256'), 'hex')"

        if vendor == "mysql":
            return "SHA2(%s, 256)"

        if vendor == "oracle":
            return "LOWER(RAWTOHEX(STANDARD_HASH(%s, 'SHA256')))"""

        if vendor in ("microsoft", "mssql", "sql_server", "mssqlms", "mssqlapi"):
            return "LOWER(CONVERT(VARCHAR(64), HASHBYTES('SHA2_256', %s), 2))"

        return "%s"
