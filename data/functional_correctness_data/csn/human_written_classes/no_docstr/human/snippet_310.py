class TruncateQuery:
    SUPPORTED_VENDORS = ('postgresql', 'mysql', 'oracle', 'microsoft')

    @classmethod
    def support_truncate_statement(cls, database_vendor) -> bool:
        return database_vendor in cls.SUPPORTED_VENDORS

    @staticmethod
    def to_sql(table_name) -> str:
        return f'TRUNCATE TABLE {table_name};'