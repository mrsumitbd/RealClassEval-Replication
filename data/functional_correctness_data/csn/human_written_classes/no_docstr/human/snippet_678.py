import logging

class FileFormat:

    def prepare_resource(self, resource):
        for field in resource.get('schema', {}).get('fields', []):
            field.update(self.PYTHON_DIALECT.get(field['type'], {}))

    def __transform_row(self, row, fields):
        try:
            return dict(((k, self.__transform_value(v, fields[k]['type'])) for k, v in row.items()))
        except Exception:
            logging.exception('Failed to transform row %r', row)
            raise

    @classmethod
    def __transform_value(cls, value, field_type):
        if value is None:
            return cls.NULL_VALUE
        serializer = cls.SERIALIZERS.get(field_type, cls.DEFAULT_SERIALIZER)
        return serializer(value)

    def write_row(self, writer, row, fields):
        transformed_row = self.__transform_row(row, fields)
        self.write_transformed_row(writer, transformed_row, fields)