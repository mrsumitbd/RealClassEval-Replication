class Definition:

    def get_table_definition(self, table):
        """Retrieve a CREATE TABLE statement for an existing table."""
        return self.fetch('SHOW CREATE TABLE {0}'.format(table))[1]

    def get_column_definition_all(self, table):
        """Retrieve the column definition statement for all columns in a table."""
        col_defs = self.get_table_definition(table).split('\n')
        return [i[0:-1].strip().replace(',', ', ') for i in col_defs if i.strip().startswith('`')]

    def get_column_definition(self, table, column):
        """Retrieve the column definition statement for a column from a table."""
        for col in self.get_column_definition_all(table):
            if col.strip('`').startswith(column):
                return col.strip(',')