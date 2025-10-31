from dictknife import DictWalker

class OpenAPI3Transformer:

    def __init__(self, schema_factory):
        self.schema_factory = schema_factory
        self.oas2transformer = OpenAPI2Transformer(schema_factory)

    def transform(self, rawtarget, depth):
        d = self.oas2transformer.transform(rawtarget, depth)
        for _, sd in DictWalker(['$ref']).walk(d):
            sd['$ref'] = sd['$ref'].replace('#/definitions/', '#/components/schemas/')
        if 'components' not in d:
            d['components'] = {}
        if 'schemas' not in d['components']:
            d['components']['schemas'] = {}
        d['components']['schemas'] = d.pop('definitions', {})
        return d