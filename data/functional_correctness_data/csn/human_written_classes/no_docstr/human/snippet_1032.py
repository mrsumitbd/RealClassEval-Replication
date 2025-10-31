class ModelStore:

    def contains_model(self, table_name, flat=False):
        if flat:
            metadata_table = FlatBase.metadata.tables.get(table_name)
        else:
            metadata_table = Base.metadata.tables.get(table_name)
        if hasattr(metadata_table, 'name'):
            metadata_table_name = metadata_table.name
        else:
            return None
        return table_name if table_name == metadata_table_name else None

    def get_model(self, table_name, flat=False):
        if flat:
            table = FlatBase.metadata.tables[table_name]
        else:
            table = Base.metadata.tables[table_name]
        return table.decl_class

    def reset_cache(self):
        Base.metadata.clear()
        FlatBase.metadata.clear()