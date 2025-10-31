import inspect

class JSONSchemaTransformer:

    def __init__(self, schema_factory):
        self.schema_factory = schema_factory

    def transform(self, rawtarget, depth):
        if not inspect.isclass(rawtarget):
            raise RuntimeError('please passing the path of model class (e.g. foo.boo:Model)')
        return self.schema_factory(rawtarget, depth=depth)