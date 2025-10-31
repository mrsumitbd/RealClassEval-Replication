import inspect

class OpenAPI2Transformer:

    def __init__(self, schema_factory):
        self.schema_factory = schema_factory

    def transform(self, rawtarget, depth):
        if inspect.isclass(rawtarget):
            return self.transform_by_model(rawtarget, depth)
        else:
            return self.transform_by_module(rawtarget, depth)

    def transform_by_model(self, model, depth):
        definitions = {}
        schema = self.schema_factory(model, depth=depth)
        if 'definitions' in schema:
            definitions.update(schema.pop('definitions'))
        definitions[schema['title']] = schema
        return {'definitions': definitions}

    def transform_by_module(self, module, depth):
        subdefinitions = {}
        definitions = {}
        for basemodel in collect_models(module):
            schema = self.schema_factory(basemodel, depth=depth)
            if 'definitions' in schema:
                subdefinitions.update(schema.pop('definitions'))
            definitions[schema['title']] = schema
        d = {}
        d.update(subdefinitions)
        d.update(definitions)
        return {'definitions': definitions}